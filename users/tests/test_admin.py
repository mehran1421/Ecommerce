from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='m.kamrani1420@gmail.com',
            password='mehran1421SSS',
            username='mehran1422'
        )

        self.admin_user = get_user_model().objects.create_superuser(
            email='m.kamrani1422@gmail.com',
            password='mehran1421SSS',
            username='mehran1421'
        )
        self.client.force_login(self.admin_user)

    def test_user_listed(self):
        """ test that users are listed on user page """

        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """

        url = reverse('admin:users_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ test that the create user page works """

        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
