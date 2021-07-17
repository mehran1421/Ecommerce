from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Ticket, QuestionAndAnswer


class ModelTicketTestCase(APITestCase):

    def setUp(self):
        self.client.post('/api/rest-auth/registration/', data={
            'username': 'mehran', 'email': 'm.dlfjs@gmail.com', 'password1': 'mehran1421', 'password2': 'mehran1421'
        })

        self.user = get_user_model().objects.get(username='mehran')
        self.token = Token.objects.create(user=self.user)
        Ticket.objects.create(title='please check my payment', status='de', user=self.user)

    def api_authentication(self):
        """ for login user """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_create_ticket(self):
        """ Test create ticket user """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/ticket/ticket/', data={
            'title': 'check my cart ',
            'status': 'de'
        })
        ticket = Ticket.objects.all()
        self.assertEqual(ticket.count(), 2)
        self.assertEqual(ticket.first().user.username, self.user.username)

    def test_show_list_ticket(self):
        """ Test show list ticket for user """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/ticket/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_update_ticket(self):
        """ user can not update ticket but superuser can update it """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        url = reverse('ticket:ticket-detail', args=[Ticket.objects.first().pk])
        response = self.client.put(url, data={
            'title': 'hello how are you?',
            'status': 'de'
        })
        self.user.is_superuser = True

        response_super_user = self.client.put(url, data={
            'title': 'hello how are you?',
            'status': 'de'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_super_user.status_code, status.HTTP_200_OK)

    def test_create_QA(self):
        """ Test for create QA object """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        res = self.client.post('/ticket/answer/', data={
            "description": "hello",
            "question": Ticket.objects.first().pk
        })
        self.assertEqual(QuestionAndAnswer.objects.all().count(), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_status_cl_create_QA(self):
        """ Test for if ticket status has cl dont create QA """

        self.api_authentication()
        self.client.force_authenticate(user=self.user)

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.post('/ticket/answer/', data={
            "description": "hello",
            "question": Ticket.objects.first().pk
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
