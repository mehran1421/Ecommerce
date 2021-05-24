from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'is_seller'
        ]

