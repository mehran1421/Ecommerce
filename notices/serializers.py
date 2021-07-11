from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import Notice


class NoticeListSerializer(ModelSerializer):
    # detail = HyperlinkedIdentityField(view_name='product:figure-detail')

    class Meta:
        model = Notice
        fields = [
            'email',
            'status',
        ]


class NoticeDetailSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'email',
            'status',
        ]


class NoticeCreateSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'email',
        ]
