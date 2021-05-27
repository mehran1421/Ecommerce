from carts.models import Cart
from carts.serializers import CartListSerializers, CartDetailSerializers
from carts.permissions import IsSuperUser
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from datetime import datetime
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from extension.utils import cacheops
from carts.models import Cart, CartItem

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


class Factor(ViewSet):
    """
    list and retrieve Carts that is_pay=True and
    user=request.user
    """

    def list(self, request):
        """
        just for user
        :param request:
        :return: list carts that is_pay=True
        """
        try:
            obj_cart = cacheops(request, 'cart-list', Cart)
            cart_obj = obj_cart.filter(user=request.user, is_pay=True)
            serializer = CartListSerializers(cart_obj, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)

    def retrieve(self, request, pk=None):
        """
        just for user that is_pay=True
        :param request:
        :param pk:
        :return: detail carts that is_pay=True
        """
        try:
            obj_cart = cacheops(request, 'cart-list', Cart)
            cart_obj = obj_cart.get(pk=pk, user=request.user, is_pay=True)
            serializer = CartDetailSerializers(cart_obj, context={'request': request}, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({'status': 'must you authentications '}, status=400)


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
