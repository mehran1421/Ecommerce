from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from extension import response
from extension.throttling import CustomThrottlingUser
from extension.exception import CustomException
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

    def get_throttles(self):
        """
        user can 4 post request per second, for create notice object
        CustomThrottlingUser ==> /throttling.py
        :return:
        """
        throttle_classes = (CustomThrottlingUser,)
        return [throttle() for throttle in throttle_classes]

    def list(self, request):
        try:
            answer = QuestionAndAnswer.objects.filter(user=request.user)
            serializer = AnswerListSerializer(answer, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        try:
            serializer = AnswerCreateSerializer(data=request.data)
            tick_pk = request.data['question']
            ticket = Ticket.objects.get(pk=tick_pk)
            if serializer.is_valid():
                if ticket.status != 'cl':
                    serializer.save(user=request.user)
                    return response.SuccessResponse(serializer.data).send()
                else:
                    return response.ErrorResponse(message='ticket is closed', status=403).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        try:
            if request.user.is_superuser:
                queryset = QuestionAndAnswer.objects.filter(pk=pk)
            else:
                queryset = QuestionAndAnswer.objects.filter(pk=pk, user=request.user)
            serializer = AnswerDetailSerializer(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        try:
            if request.user.is_superuser:
                answer = QuestionAndAnswer.objects.get(pk=pk)
            else:
                answer = QuestionAndAnswer.objects.get(pk=pk, user=request.user)

            tick_pk = int(request.data['question'])
            ticket = Ticket.objects.get(pk=tick_pk)
            serializer = AnswerDetailSerializer(answer, data=request.data)
            if serializer.is_valid():
                if ticket.status != 'cl':
                    serializer.save()
                    return response.SuccessResponse(serializer.data).send()
                else:
                    return response.ErrorResponse(message='ticket is closed', status=403).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        try:
            if request.user.is_superuser:
                answer = QuestionAndAnswer.objects.get(pk=pk)
            else:
                answer = QuestionAndAnswer.objects.get(pk=pk, user=request.user)
                if answer.question.status == 'cl':
                    return response.ErrorResponse(message='you can not delete ticketing object with status cl',
                                                  status=403).send()

            answer.delete()
            return response.SuccessResponse(message='Deleted object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()


class TicketViews(ViewSet):
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_throttles(self):
        """
        user can 4 post request per second, for create notice object
        CustomThrottlingUser ==> /throttling.py
        :return:
        """
        throttle_classes = (CustomThrottlingUser,)
        return [throttle() for throttle in throttle_classes]

    def list(self, request):
        try:
            if request.user.is_superuser:
                ticket = Ticket.objects.all()
            else:
                ticket = Ticket.objects.filter(user=request.user)
            serializer = TicketListSerializer(ticket, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        try:
            serializer = TicketCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(status='de', user=request.user)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        try:
            if request.user.is_superuser:
                queryset = Ticket.objects.filter(pk=pk)
            else:
                queryset = Ticket.objects.filter(pk=pk, user=request.user)
            serializer = TicketDetailSerializer(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        try:
            if request.user.is_superuser:
                ticket = Ticket.objects.get(pk=pk)
            else:
                ticket = Ticket.objects.get(pk=pk, user=request.user)

            serializer = TicketDetailSerializer(ticket, context={'request': request}, data=request.data)
            if serializer.is_valid(raise_exception=True):
                if request.user.is_superuser:
                    serializer.save()
                else:
                    serializer.save(status='bn', user=request.user)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

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
