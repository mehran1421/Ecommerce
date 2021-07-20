from django.db import models
from users.models import User


class TicketCreatorTime(models.Model):
    """
    abstract class for inheritance
    user and create is Common in Ticket and QuestionAndAnswer
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Ticket(TicketCreatorTime):
    """
    if status == cl ==> ticket is close and can not create or update it
    elif status == de ==> ticket is Waiting for answer superuser
    elif status == bs ==> ticket Reviewed by superuser and Wait user that answer him
    """
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
    """
    each Ticket have many QuestionAndAnswer object
    that mean Ticket ==>([QA1,QA2,...]) that each QA object are for superuser or user
    """
    description = models.TextField()
    question = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        ordering = ['create']
