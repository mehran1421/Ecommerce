from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from extension.permissions import IsSuperUserOrOwnerCart
from .serializers import (
    UserListSerializers,
    UserDetailSerializers
)

User = get_user_model()


class UserViews(ViewSet):
    permission_classes = (IsSuperUserOrOwnerCart,)

    lookup_field = 'username'

    def list(self, request):
        obj = User.objects.all()
        serializer = UserListSerializers(obj, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        obj = User.objects.all()
        queryset = obj.filter(username=username)
        serializer = UserDetailSerializers(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
