from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from extension.utils import cacheops
from django.contrib.auth import get_user_model
from carts.permissions import IsSuperUser
from .serializers import (
    UserListSerializers,
    UserDetailSerializers
)

User = get_user_model()


class UserViews(ViewSet):
    permission_classes = (IsSuperUser,)

    lookup_field = 'username'

    def list(self, request):
        obj = cacheops(request, 'user-list', User)
        serializer = UserListSerializers(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        obj = cacheops(request, 'user-list', User)
        queryset = obj.filter(username=username)
        serializer = UserDetailSerializers(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
