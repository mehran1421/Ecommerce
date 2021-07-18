from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Product, Category
from ..serializers import CategoryInputSerializer


class ModelItemTestCase(APITestCase):

    def setUp(self):
        self.client.post('/api/rest-auth/registration/', data={
            'username': 'mehran', 'email': 'm.dlfjs@gmail.com', 'password1': 'mehran1421', 'password2': 'mehran1421'
        })

        self.user = get_user_model().objects.get(username='mehran')
        self.token = Token.objects.create(user=self.user)
        url_product = reverse("product:product-list")

        self.cat = Category.objects.create(title='mobile', slug='mobile', status=True, position=1)
        self.product = Product.objects.create(title='samsung j7', description='android app', seller=self.user,
                                              price=1.54,
                                              thumbnail="/media/images/1_d3HHH29.jpg")
        self.product.category.set([self.cat])

    def api_authentication(self):
        """ for login user """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_list_category(self):
        """ Test list product """

        res = self.client.get(reverse('product:category-list'))
        category = Category.objects.all().count()

        self.assertEqual(category, 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        """ Test just superuser can create category objects """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        self.client.post('/category/', data={
            'title': 'mobile2',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })

        counter = Category.objects.all().count()
        self.assertEqual(counter, 1)

        self.user.is_superuser = True
        self.client.post('/category/', data={
            'title': 'mobile2',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })
        counter = Category.objects.all().count()
        self.assertEqual(counter, 2)

    def test_update_category(self):
        """ Test update category """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('product:category-detail', args=[Category.objects.first().slug])
        res = self.client.put(url, {
            'title': 'my mobile',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })
        cat = Category.objects.first()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(cat.title, 'my mobile')

    def test_delete_category(self):
        """ Test delete category """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('product:category-detail', args=[Category.objects.first().slug])
        res = self.client.delete(url)
        cat = Category.objects.all().count()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(cat, 0)

    def test_list_product(self):
        """ Test list product """

        res = self.client.get(reverse('product:product-list'))
        category = Product.objects.all().count()

        self.assertEqual(category, 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def update_product(self):
        """ Test update product """

        self.user.is_superuser = True
        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        url = url = reverse('product:product-detail', args=[Product.objects.first().slug])
        res = self.client.put(url, data={
            'title': 'samsung sfsff', 'description': 'android app',
            'price': 1.54,
            'thumbnail': "/media/images/1_d3HHH29.jpg"
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_products(self):
        """ Test create product by superuser """

        self.user.is_superuser = True
        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        url = reverse('product:product-list')
        res = self.client.post(url, data={
            'title': 'samsung jffff7',
            'description': 'os:android',
            'price': 0.18,
            'thumbnail': "/media/images/1_d3HHH29.jpg"
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_delete_product(self):
        """ Test for delete product by superuser """

        self.user.is_superuser = True
        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        res = self.client.delete('/product/samsung-j7/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
