from celery import shared_task
from django.core.mail import EmailMessage
from .models import Notice
from items.models import Product


@shared_task
def send_email():
    notice = Notice.objects.filter(status=True)
    product = Product.objects.filter(status=True, choice='p')[:5]
    emails = []
    message = f"my product {0}".format(product)
    for i in notice:
        emails.append(str(i.email))

    email = EmailMessage(
        'new product', message, to=emails
    )
    return email.send()
