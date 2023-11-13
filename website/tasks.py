# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Record

@shared_task
def send_delayed_emails(subject, message):
    records = Record.objects.all()

    for record in records:
        send_mail(subject, message, 'from@example.com', [record.email])
