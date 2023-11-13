from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

@shared_task
def send_delayed_email(record_id, subject, message):
    from .models import Record

    record = Record.objects.get(pk=record_id)
    send_mail(subject, message, 'from@example.com', [record.email])
