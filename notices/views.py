from rest_framework.viewsets import ViewSet
from .serializers import (
    NoticeCreateSerializer,
    NoticeDetailSerializer,
    NoticeListSerializer
)
from .models import Notice
from extension.permissions import IsSuperUserOrIsSeller
from .throttling import CustomThrottlingUser
from extension.exception import CustomException
from extension import response


class NoticeViews(ViewSet):
    """
    all user can create notice object but can not show list or update it
    use throttling in this class ==> each user can 4 request for create in 1 second

    """

    def get_permissions(self):
        """
        IsAdminUser for created by rest framework by default
        just superuser can access to site
        :return:
        """
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            permission_classes = (IsSuperUserOrIsSeller,)
        else:
            permission_classes = ()

        return [permission() for permission in permission_classes]

    def get_throttles(self):
        """
        user can 4 post request per second, for create notice object
        CustomThrottlingUser ==> /throttling.py
        :return:
        """
        if self.action == 'create':
            throttle_classes = (CustomThrottlingUser,)
        else:
            throttle_classes = ()

        return [throttle() for throttle in throttle_classes]

    def list(self, request):
        """
        show list all notices object for superuser
        :param request:
        :return:
        """
        try:
            notice = Notice.objects.all()
            serializer = NoticeListSerializer(notice, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def create(self, request):
        """
        create notice object by all user
        when superuser has not approved (status == False) ==> dont send email for user
        :param request:
        :return:
        """
        try:
            serializer = NoticeCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(status=False)
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, pk=None):
        """
        detail object for superuser
        :param request:
        :param pk:
        :return:
        """
        try:
            queryset = Notice.objects.filter(pk=pk)
            serializer = NoticeDetailSerializer(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def update(self, request, pk=None):
        """
        superuser can update all object notices
        :param request:
        :param pk:
        :return:
        """
        try:
            notice = Notice.objects.get(pk=pk)
            serializer = NoticeDetailSerializer(notice, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def destroy(self, request, pk=None):
        """
        superuser can delete notices object
        :param request:
        :param pk:
        :return:
        """
        try:
            notice = Notice.objects.get(pk=pk)
            notice.delete()
            return response.SuccessResponse(message='Deleted object').send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()
