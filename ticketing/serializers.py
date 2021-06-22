from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Ticket,
    Answare
)
from users.serializers import UserListSerializers


class TicketListSerializer(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='ticket:ticket-detail')

    class Meta:
        model = Ticket
        fields = [
            'detail',
            'user',
            'create',
            'title',
            'status',
        ]


class TicketDetailSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'user',
            'description',
            'create',
            'title',
            'status',
        ]


class TicketCreateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'user',
            'description',
            'title',
        ]


class AnswerListSerializer(ModelSerializer):
    # detail = HyperlinkedIdentityField(view_name='product:figure-detail')

    class Meta:
        model = Answare
        fields = [
            'user',
            'create',
            'ticket',
        ]


class AnswerDetailSerializer(ModelSerializer):
    class Meta:
        model = Answare
        fields = [
            'user',
            'description',
            'create',
            'status',
        ]


class AnswerCreateSerializer(ModelSerializer):
    class Meta:
        model = Answare
        fields = [
            'user',
            'description',
            'status',
        ]
