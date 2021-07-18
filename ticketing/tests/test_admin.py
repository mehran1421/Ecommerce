from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Ticket, QuestionAndAnswer
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

    def test_ticket_listed(self):
        """ test that ticket objects are listed """

        self.client.post('/ticket/ticket/', data={
            'title': 'check my cart ',
            'status': 'de'
        })
        res = self.client.get('/secret/ticketing/ticket/')
        ticket = Ticket.objects.first()

        self.assertContains(res, ticket.title)
