from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import (
    Ticket,
    QuestionAndAnswer
)


class TicketListSerializer(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='ticket:ticket-detail')

    class Meta:
        model = Ticket
        fields = [
            'detail',
            'title',
            'create',
            'status',
        ]


class TicketDetailSerializer(ModelSerializer):
    answer = HyperlinkedIdentityField(view_name='ticket:ticket-answer-ticket')

    def get_username(self, obj):
        return obj.user.username

    user = SerializerMethodField('get_username')

    class Meta:
        model = Ticket
        fields = [
            'answer',
            'title',
            'user',
            'create',
            'status',
        ]


class TicketCreateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'status',
            'title',
        ]


class AnswerListSerializer(ModelSerializer):
    detail = HyperlinkedIdentityField(view_name='ticket:answer-detail')

    class Meta:
        model = QuestionAndAnswer
        fields = [
            'detail',
            'user',
            'create',
            'question',
        ]


class AnswerDetailSerializer(ModelSerializer):
    class Meta:
        model = QuestionAndAnswer
        fields = [
            'user',
            'create',
            'description',
            'question',
        ]


class AnswerCreateSerializer(ModelSerializer):
    class Meta:
        model = QuestionAndAnswer
        fields = [
            'description',
            'question',
        ]
