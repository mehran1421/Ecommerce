from django.db import models


class Notice(models.Model):
    email = models.EmailField(unique=True, max_length=20)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)
