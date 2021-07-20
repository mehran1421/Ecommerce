from rest_framework.viewsets import ViewSet
from .serializers import (
    NoticeCreateSerializer,
    NoticeDetailSerializer,
    NoticeListSerializer
)
from .models import Notice
from extension.permissions import IsSuperUserOrOwnerCart
from .throttling import CustomThrottlingUser
from extension.exception import CustomException
from extension import response


class NoticeViews(ViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrOwnerCart,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def get_throttles(self):
        """
        user can 4 post request per second, for create notice object
        :return:
        """
        if self.action == 'create':
            throttle_classes = (CustomThrottlingUser,)
        else:
            throttle_classes = ()

        return [throttle() for throttle in throttle_classes]

    def list(self, request):
        try:
            notice = Notice.objects.all()
            serializer = NoticeListSerializer(notice, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        try:
            serializer = NoticeCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(status=False)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        try:
            queryset = Notice.objects.filter(pk=pk)
            serializer = NoticeDetailSerializer(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        try:
            notice = Notice.objects.get(pk=pk)
            serializer = NoticeDetailSerializer(notice, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        try:
            notice = Notice.objects.get(pk=pk)
            notice.delete()
            return response.SuccessResponse(message='Deleted object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()
