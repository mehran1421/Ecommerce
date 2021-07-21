from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from config.base_api_test import BaseTest
from rest_framework import status
from django.urls import reverse
from ..models import Cart, CartItem
from items.models import Product, Category


class ModelItemTestCase(BaseTest):

    def test_create_cart(self):
        """ Test for create cart by user is_pay=False just one """

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/cart/cart/', data={
            'user': get_user_model().objects.first().pk,
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Cart.objects.all().count(), 1)

    def test_list_cart(self):
        """ Test list carts that is_pay is False """

        self.client.force_authenticate(user=self.user)

        res = self.client.get(reverse('carts:cart-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_cart(self):
        """ Test update cart by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('carts:cart-detail', args=[Cart.objects.first().pk])
        res = self.client.put(url, {
            'user': get_user_model().objects.first().pk,
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_cart(self):
        """ Test delete cart """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('carts:cart-detail', args=[Cart.objects.first().pk])
        self.client.delete(url)
        self.assertEqual(Cart.objects.all().count(), 0)

    def test_create_cart_item(self):
        """ Test create cart item by user """

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/cart/cartItem/', data={
            'cart': Cart.objects.first().pk,
            'item': Product.objects.first().pk,
            'quantity': 2
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.all().count(), 2)

    def test_list_cart_item(self):
        """ Test get list for user """

        self.client.force_authenticate(user=self.user)

        res = self.client.get(reverse('carts:cart-item-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_cart_item(self):
        """ Test delete cart item by user """

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(reverse('carts:cart-item-detail', args=[CartItem.objects.first().pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.all().count(), 0)
