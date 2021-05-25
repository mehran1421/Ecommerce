from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListSerializers(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='user:user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'email',
            'is_seller'
        ]


class UserDetailSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
