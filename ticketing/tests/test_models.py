from django.contrib.auth import get_user_model
from config.base_api_test import BaseTest
from rest_framework import status
from django.urls import reverse
from ..models import Ticket, QuestionAndAnswer
from ..serializers import TicketCreateSerializer, AnswerCreateSerializer


class ModelTicketTestCase(BaseTest):

    def test_create_ticket(self):
        """ Test create ticket user """

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

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/ticket/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_update_ticket(self):
        """ user can not update ticket but superuser can update it """

        self.client.force_authenticate(user=self.user)

        url = reverse('ticket:ticket-detail', args=[Ticket.objects.first().pk])
        response = self.client.put(url, data={
            'title': 'hello how are you?',
            'status': 'de'
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_update_ticket(self):
        """ Test superuser can update it """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_seller = True
        self.user.is_active = True

        url = reverse('ticket:ticket-detail', args=[Ticket.objects.first().pk])
        response_super_user = self.client.put(url, data={
            'title': 'hello how are you?',
            'status': 'de'
        })

        self.assertEqual(response_super_user.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.first().title, 'hello how are you?')

    def test_other_user_delete_ticket(self):
        """ user can not delete ticket but superuser can delete it """

        self.client.force_authenticate(user=self.user)

        url = reverse('ticket:ticket-detail', args=[Ticket.objects.first().pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_ticket(self):
        """ Test superuser can delete it """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_seller = True
        self.user.is_active = True

        url = reverse('ticket:ticket-detail', args=[Ticket.objects.first().pk])
        response_super_user = self.client.delete(url)

        self.assertEqual(response_super_user.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.all().count(), 0)

    def test_create_QA(self):
        """ Test for create QA object """

        self.client.force_authenticate(user=self.user)

        res = self.client.post('/ticket/answer/', data={
            "description": "hi how are you?",
            "question": Ticket.objects.first().pk
        })
        self.assertEqual(QuestionAndAnswer.objects.all().count(), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_status_cl_create_QA(self):
        """ Test for if ticket status has cl dont create QA """

        self.client.force_authenticate(user=self.user)

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.post('/ticket/answer/', data={
            "description": "hi check my cart",
            "question": Ticket.objects.first().pk
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_QA_object(self):
        """ Test can delete object """

        self.client.force_authenticate(user=self.user)

        res = self.client.delete(reverse('ticket:answer-detail', args=[QuestionAndAnswer.objects.first().pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_QA_ticket_closed(self):
        """ Test can not user delete QA object when ticket status is cl """

        self.client.force_authenticate(user=self.user)

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.delete(reverse('ticket:answer-detail', args=[QuestionAndAnswer.objects.first().pk]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_QA_superuser_ticket_closed(self):
        """ Test can not user delete QA object by superuser when ticket status is cl """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_seller = True
        self.user.is_active = True

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.delete(reverse('ticket:answer-detail', args=[QuestionAndAnswer.objects.first().pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_QA_ticket_closed(self):
        """ Test can not user update QA object when ticket status is cl """

        self.client.force_authenticate(user=self.user)

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.put(reverse('ticket:answer-detail', args=[QuestionAndAnswer.objects.first().pk]), data={
            'description': 'my name is mehran',
            "question": ticket.pk
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_QA_superuser_ticket_closed(self):
        """ Test can not user delete QA object by superuser when ticket status is cl """

        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_seller = True
        self.user.is_active = True

        ticket = Ticket.objects.first()
        ticket.status = 'cl'
        ticket.save()

        res = self.client.put(reverse('ticket:answer-detail', args=[QuestionAndAnswer.objects.first().pk]), data={
            'description': 'my name is mehran',
            'user': self.user,
            "question": ticket.pk
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_output_list_serilizer(self):
        """ Test output serializer product """
        data = {
            'title': 'hi',
            'status': 'de',
        }
        serializer = TicketCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['title'], data['title'])

    def test_output_Qa_list_serilizer(self):
        """ Test output serializer product """
        data = {
            'description': 'hello my name is mehran',
            'question': self.ticket.pk,
        }
        serializer = AnswerCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['description'], data['description'])
