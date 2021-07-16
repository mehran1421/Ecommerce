import json
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from ..serializers import NoticeListSerializer
from rest_framework import status
from ..models import Notice


class ViewNoticesTestCase(APITestCase):

    def test_output_list_serilizer(self):
        data = {
            "email": "ssf@gmail.com"
        }
        serializer = NoticeListSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['email'], data['email'])
