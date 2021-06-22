from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .serializers import (
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
    AnswerListSerializer,
)
from .models import (
    Ticket,
    Answare
)


class TicketViews(ViewSet):
    # authintication
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
                serializer.save(status='bn', user=request.user)
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
        if serializer.is_valid():
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
