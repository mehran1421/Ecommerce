from django.contrib.auth import get_user_model
from config.base_api_test import BaseTest
from rest_framework import status
from django.urls import reverse
from ..models import Product, Category, FigureField
from ..serializers import CategoryInputSerializer


class ModelItemTestCase(BaseTest):

    def test_list_category(self):
        """ Test list product """

        res = self.client.get(reverse('product:category-list'))
        category = Category.objects.all().count()

        self.assertEqual(category, 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        """ Test just user can create category objects """

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/category/', data={
            'title': 'mobile2',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })

        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_create_category(self):
        """ Test just superuser can create category objects """

        self.client.force_authenticate(user=self.user)

        self.user.is_superuser = True
        response = self.client.post('/category/', data={
            'title': 'mobile2',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })
        self.assertEqual(Category.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        """ Test update category by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('product:category-detail', args=[Category.objects.first().slug])
        res = self.client.put(url, {
            'title': 'my mobile',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.first().title, 'my mobile')

    def test_delete_category(self):
        """ Test delete category by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('product:category-detail', args=[Category.objects.first().slug])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_list_product(self):
        """ Test list product """

        res = self.client.get(reverse('product:product-list'))
        product = Product.objects.all().count()

        self.assertEqual(product, 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def update_product(self):
        """ Test update product """

        self.client.force_authenticate(user=self.user)

        url = reverse('product:product-detail', args=[Product.objects.first().slug])
        res = self.client.put(url, data={
            'title': 'samsung sfsff', 'description': 'android app',
            'price': 1.54,
            'thumbnail': "/media/images/1_d3HHH29.jpg"
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_products(self):
        """ Test create product by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        url = reverse('product:product-list')
        res = self.client.post(url, data={
            'title': 'samsung jffff7',
            'description': 'os:android',
            'price': 0.18,
            'category': [self.cat.pk],
            'thumbnail': 'http://127.0.0.1:8000/media/images/1_d3HHH29.jpg'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_delete_product(self):
        """ Test for delete product by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        res = self.client.delete('/product/samsung-j7/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_figure_list_request(self):
        """ Test figure list request by user """

        response = self.client.get('/figure/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_figure_create(self):
        """ Test can not create figure by user """

        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse('product:figure-list'), data={
            'type_product': 'android'
        })

        self.assertEqual(FigureField.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_figure_create(self):
        """ Test can not create figure by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        response = self.client.post(reverse('product:figure-list'), data={
            'type_product': 'android'
        })

        self.assertEqual(FigureField.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_figure_superuser(self):
        """ Test update figure object by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        figure = FigureField.objects.create(type_product='android')
        response = self.client.put(reverse('product:figure-detail', args=[figure.pk]), data={
            'type_product': 'backend'
        })

        self.assertEqual(FigureField.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FigureField.objects.first().type_product, 'backend')

    def test_delete_figure_superuser(self):
        """ Test delete figure object by superuser """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True

        figure = FigureField.objects.create(type_product='android')
        response = self.client.delete(reverse('product:figure-detail', args=[figure.pk]))

        self.assertEqual(FigureField.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_output_category_list_serilizer(self):
        """ Test output serializer category """

        data = {
            'title': 'mobile2',
            'slug': 'mobile2',
            'status': True,
            'position': 2,
        }
        serializer = CategoryInputSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['title'], data['title'])
