from carts.permissions import IsSuperUser
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.db.models import Q
from datetime import datetime
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from carts.models import Cart
from carts.serializers import (
    CartListSerializers,
    CartDetailSerializers
)

try:
    from config.settings.keys import MERCHANT
except Exception:
    MERCHANT = "Some kind of hash"

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for realy server.


class Factors(ViewSet):
    """
    list and retrieve Carts that is_pay=True and
    user=request.user
    """

    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            permission_classes = (IsSuperUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        just for user
        and superuser can show all carts that is_pay=True
        :param request:
        :return: list carts that is_pay=True
        """
        try:
            obj_cart = Cart.objects.all()
            if request.user.is_superuser:
                cart_obj = obj_cart.filter(is_pay=True)
            else:
                cart_obj = obj_cart.filter(user=request.user, is_pay=True)
            serializer = CartListSerializers(cart_obj, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        """
        just for user that is_pay=True
        and superuser can show all carts that is_pay=True
        :param request:
        :param pk:
        :return: detail carts that is_pay=True
        """
        try:
            obj_cart = Cart.objects.all()
            if request.user.is_superuser:
                cart_obj = obj_cart.get(pk=pk, is_pay=True)
            else:
                cart_obj = obj_cart.get(pk=pk, user=request.user, is_pay=True)
            serializer = CartDetailSerializers(cart_obj, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def update(self, request, pk=None):
        """
        just superuser can update list carts that is_pay=True
        :param request:
        :param pk:
        :return: update object with pk=pk
        """
        try:
            obj = Cart.objects.all()
            cart = obj.get(pk=pk, is_pay=True)
            serializer = CartDetailSerializers(cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'}, status=200)
            return Response({'status': 'Internal Server Error'}, status=500)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def destroy(self, request, pk=None):
        """
        just super user can delete it
        :param request:
        :param pk:
        :return: delete object with pk=pk and is_pay=True
        """
        try:
            obj = Cart.objects.all()
            obj.get(pk=pk, is_pay=True).delete()
            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    @action(detail=False, methods=['get'], name='factor-search')
    def pay_search(self, request):
        # http://localhost:8000/payment/factor/pay_search/?search=mehran
        obj = Cart.objects.all()
        query = self.request.GET.get('search')
        object_list = obj.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(products__title__icontains=query) |
            Q(products__title__icontains=query),
            is_pay=True
        )
        if request.user.is_superuser:
            serializer = CartListSerializers(object_list, context={'request': request}, many=True)
        else:
            objUser = object_list.filter(user=request.user)
            serializer = CartListSerializers(objUser, context={'request': request}, many=True)
        return Response(serializer.data)


def send_request(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is not None:
        amount = cart.subtotal
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile,
                                               f"{CallbackURL}/{cart.pk}/")
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))

    return Response("access denide", status=403)


def verify(request, *args, **kwargs):
    pk = kwargs.get('pk')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            """
            my code for pay cart
            ===================================================
            """
            cart = Cart.objects.get(pk=pk)
            cart.is_pay = True
            cart.timestamp = datetime.now()
            cart.save()
            """
            ===================================================
            """
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
