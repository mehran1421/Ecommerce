from django.db import models
from users.models import User


class TicketCreatorTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Ticket(TicketCreatorTime):
    STATUS_CHOICE = (
        ('cl', 'بسته شده'),
        ('de', 'در انتظار'),
        ('bs', 'بررسی شده'),
    )

    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE)

    class Meta:
        ordering = ['create']

    def __str__(self):
        return self.title


class QuestionAndAnswer(TicketCreatorTime):
    description = models.TextField()
    question = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        ordering = ['create']
