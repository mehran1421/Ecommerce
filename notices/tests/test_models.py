from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Notice


class UserNoticesTestCase(APITestCase):

    def setUp(self):
        self.client.post('/api/rest-auth/registration/', data={
            'username': 'mehran', 'email': 'm.dlfjs@gmail.com', 'password1': 'mehran1421', 'password2': 'mehran1421'
        })
        self.super_user = get_user_model().objects.get(username='mehran')
        self.super_user.is_superuser = True
        self.super_user.save()
        self.token = Token.objects.create(user=self.super_user)

        data = {
            'email': 'm.ka@gmail.com',
        }
        self.response = self.client.post('/notice/notice/', data=data)

    def api_authentication(self):
        """ for login user """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_create_notice(self):
        """ Test create notice with email """

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_status_model_notice(self):
        """ Test for status is False after create """

        notice = Notice.objects.get(email='m.ka@gmail.com')
        self.assertFalse(notice.status)
        self.assertEqual(notice.pk, 2)

    def test_user_update_delete(self):
        """ Test that can not user update notice object """

        user_update = self.client.put('/notice/notice/2/')
        user_delete = self.client.delete('/notice/notice/2/')

        self.assertEqual(user_update.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_super_user_update_delete(self):
        """ Test that superuser can update or delete notice object """

        self.api_authentication()
        self.client.force_authenticate(user=self.super_user)

        user_update = self.client.put('/notice/notice/3/', data={
            'email': 'fs@gmail.com'
        })
        user_delete = self.client.delete('/notice/notice/3/')

        self.assertEqual(user_update.status_code, status.HTTP_200_OK)
        self.assertEqual(user_delete.status_code, status.HTTP_200_OK)
