from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .serializers import (
    NoticeCreateSerializer,
    NoticeDetailSerializer,
    NoticeListSerializer
)
from .models import Notice
from carts.permissions import IsSuperUser


class NoticeViews(ViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            permission_classes = (IsSuperUser,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def list(self, request):
        notice = Notice.objects.all()
        serializer = NoticeListSerializer(notice, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = NoticeCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(status=False)
            else:
                return Response({'status': 'Bad Request'}, status=400)

            return Response({'status': 'ok'}, status=200)
        except Exception:
            return Response({'status': 'Internal Server Error'}, status=500)

    def retrieve(self, request, pk=None):
        queryset = Notice.objects.filter(pk=pk)
        serializer = NoticeDetailSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        notice = Notice.objects.get(pk=pk)

        serializer = NoticeDetailSerializer(notice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'}, status=200)
        return Response({'status': 'Internal Server Error'}, status=500)

    def destroy(self, request, pk=None):
        notice = Notice.objects.get(pk=pk)
        notice.delete()
        return Response({'status': 'ok'}, status=200)