from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from extension.permissions import IsSuperUserOrOwnerCart
from .serializers import (
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    AnswerListSerializer,
    AnswerDetailSerializer,
    AnswerCreateSerializer

)
from .models import (
    Ticket,
    QuestionAndAnswer
)


class QuestionAnswerViews(ViewSet):
    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        answer = QuestionAndAnswer.objects.filter(user=request.user)
        serializer = AnswerListSerializer(answer, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = AnswerCreateSerializer(data=request.data)
            tick_pk = request.data['question']
            ticket = Ticket.objects.get(pk=tick_pk)
            if serializer.is_valid() and ticket.status != 'cl':
                serializer.save(user=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            queryset = QuestionAndAnswer.objects.filter(pk=pk)
        else:
            queryset = QuestionAndAnswer.objects.filter(pk=pk, user=request.user)
        serializer = AnswerDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if request.user.is_superuser:
            answer = QuestionAndAnswer.objects.get(pk=pk)
        else:
            answer = QuestionAndAnswer.objects.get(pk=pk, user=request.user)

        serializer = AnswerDetailSerializer(answer, data=request.data)
        if serializer.is_valid() and serializer.data.get('question').status != 'cl':
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        if request.user.is_superuser:
            answer = QuestionAndAnswer.objects.get(pk=pk)
        else:
            answer = QuestionAndAnswer.objects.get(pk=pk, user=request.user)
            if answer.question.status == 'cl':
                return Response({'status': 'ticket is closed'}, status=403)

        answer.delete()
        return Response({'status': 'ok'}, status=200)


class TicketViews(ViewSet):
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'retrieve']:
            permission_classes = (IsSuperUserOrOwnerCart,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def list(self, request):
        if request.user.is_superuser:
            ticket = Ticket.objects.all()
        else:
            ticket = Ticket.objects.filter(user=request.user)
        serializer = TicketListSerializer(ticket, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = TicketCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(status='de', user=request.user)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            queryset = Ticket.objects.filter(pk=pk)
        else:
            queryset = Ticket.objects.filter(pk=pk, user=request.user)
        serializer = TicketDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        if request.user.is_superuser:
            ticket = Ticket.objects.get(pk=pk)
        else:
            ticket = Ticket.objects.get(pk=pk, user=request.user)

        serializer = TicketDetailSerializer(ticket, data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(status='bn', user=request.user)
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        if request.user.is_superuser:
            ticket = Ticket.objects.get(pk=pk)
        else:
            ticket = Ticket.objects.get(pk=pk, user=request.user)
        ticket.delete()
        return Response({'status': 'ok'}, status=200)

    @action(detail=True, methods=['get'], name='answer-ticket')
    def answer_ticket(self, request, pk=None):
        queryset = Ticket.objects.get(pk=pk)
        answer = QuestionAndAnswer.objects.filter(question=queryset)
        serializer = AnswerListSerializer(answer, context={'request': request}, many=True)
        return Response(serializer.data)
