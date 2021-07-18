from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Notice
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='m.kamrani1422@gmail.com',
            password='mehran1421SSS',
            username='mehran1421'
        )
        self.client.force_login(self.admin_user)

    def test_notices_listed(self):
        """ tests that noticed objects are listed """

        notice = Notice.objects.create(email='mss@gmail.com')

        res = self.client.get('/secret/notices/notice/')

        self.assertContains(res, notice.email)

