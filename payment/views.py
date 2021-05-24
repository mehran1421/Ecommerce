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

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for realy server.


class PayViews(ViewSet):
    permission_classes = (IsSuperUser,)

    def list(self, request):
        obj = cache.get('cart-list', None)
        if obj is None:
            obj = Cart.objects.all()
            cache.set('cart-list', obj)
        cart = obj.filter(is_pay=True)
        serializer = CartListSerializers(cart, context={'request': request}, many=True)
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
