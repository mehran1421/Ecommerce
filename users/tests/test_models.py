# from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

#
# class ModelTests(TestCase):
#     def setUp(self):
#         """ Variables that were used more than 2 times and to comply with the DRY rule """
#
#         self.email = 'm.kamrani1422@gmail.com'
#         self.password = 'mehran1421SSS'
#         self.user = get_user_model().objects.create_user(
#             email=self.email,
#             username='ali21',
#             password=self.password
#         )
#
#     def test_create_user_with_email(self):
#         """ Test Creating a new User with email """
#
#         self.assertEqual(self.user.email, self.email)
#         self.assertTrue(self.user.check_password(self.password))
#         self.assertTrue(get_user_model().objects.all().count(), 1)
#
#     def test_create_user_with_email_normalized(self):
#         """ Test the email for a new user is normalized """
#
#         self.assertEqual(self.user.email, self.email.lower())
#
#     def test_create_new_superuser(self):
#         """ Test creating a new superuser """
#
#         user = get_user_model().objects.create_superuser(
#             username='amirali',
#             email='m.kamrani1421@gmail.com',
#             password='mehran1421SSS'
#         )
#         self.assertTrue(user.is_superuser)
#         self.assertTrue(user.is_staff)


# class RegistrationTestCase(APITestCase):
#     def test_registration(self):
#         data = {
#             'username': 'mehran', 'email': 'm.kamrani1379@gmail.com', 'password1': 'mehran1420',
#             'password2': 'mehran1420',
#         }
#         response = self.client.post('/api/rest-auth/registration/', data=data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
