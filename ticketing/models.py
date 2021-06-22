from django.db import models
from users.models import User
from django.utils import timezone


class TimeTextField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Ticket(TimeTextField):
    STATUS_CHOICE = (
        ('cl', 'بسته شده'),
        ('bn', 'بررسی نشده'),
        ('bs', 'بررسی شده'),
    )

    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['create']


class Answare(TimeTextField):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket.title
