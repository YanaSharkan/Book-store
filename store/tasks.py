from celery import shared_task

from django.core.mail import send_mail


@shared_task()
def send_reminder(email, text):
    send_mail(
        'Reminder',
        text,
        'test@test.com',
        [email],
        fail_silently=False,
    )
