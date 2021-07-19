from ..serializers import NoticeListSerializer
from config.base_api_test import BaseTest
from django.urls import reverse
from rest_framework import status
from ..models import Notice


class ModelNoticesTestCase(BaseTest):

    def test_create_notice(self):
        """ Test create notice with email """
        response = self.client.post('/notice/notice/', data={
            'email': 'm.j@gmail.com',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notice.objects.all().count(), 2)

    def test_status_model_notice(self):
        """ Test for status is False after create """

        notice = Notice.objects.get(email='m.ka@gmail.com')
        self.assertFalse(notice.status)

    def test_user_update_delete(self):
        """
        Test that can not user update notice object
        superuser can update it but user can not update it
        """

        self.client.force_authenticate(self.user)
        user_update = self.client.put(reverse('notice:notice-detail', args=[Notice.objects.first().pk]), data={
            'email': 'ss@gmail.com'
        })

        self.assertEqual(user_update.status_code, status.HTTP_403_FORBIDDEN)
        self.user.is_superuser = True

        super_user_update = self.client.put(reverse('notice:notice-detail', args=[Notice.objects.first().pk]), data={
            'email': 'ss@gmail.com'
        })

        self.assertEqual(super_user_update.status_code, status.HTTP_200_OK)

    def test_user_delete_notice_object(self):
        """
        Test can user delete object
        superuser can delete it but user can not delete it
        """

        self.client.force_authenticate(self.user)
        user_update = self.client.delete(reverse('notice:notice-detail', args=[Notice.objects.first().pk]))

        self.assertEqual(user_update.status_code, status.HTTP_403_FORBIDDEN)
        self.user.is_superuser = True

        super_user_update = self.client.delete(reverse('notice:notice-detail', args=[Notice.objects.first().pk]))

        self.assertEqual(super_user_update.status_code, status.HTTP_200_OK)

    def test_output_list_serilizer(self):
        """ Test output serializer """
        data = {
            "email": "vvf@gmail.com"
        }
        serializer = NoticeListSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['email'], data['email'])
