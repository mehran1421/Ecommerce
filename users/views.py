from rest_framework.viewsets import ViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from extension.exception import CustomException
from extension import response
from extension.throttling import CustomThrottlingUser
from .serializers import (
    UserListSerializers,
    UserDetailSerializers
)

User = get_user_model()


class UserViews(ViewSet):
    permission_classes = (IsAdminUser,)

    def get_throttles(self):
        """
        user can 4 post request per second, for create notice object
        CustomThrottlingUser ==> /throttling.py
        :return:
        """
        throttle_classes = (CustomThrottlingUser,)
        return [throttle() for throttle in throttle_classes]

    lookup_field = 'username'

    def list(self, request):
        try:
            obj = User.objects.all()
            serializer = UserListSerializers(obj, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()

    def retrieve(self, request, username=None):
        try:
            obj = User.objects.all()
            queryset = obj.filter(username=username)
            serializer = UserDetailSerializers(queryset, context={'request': request}, many=True)
            return response.SuccessResponse(serializer.data).send()
        except CustomException as e:
            return response.ErrorResponse(message=e.detail, status=e.status_code).send()
