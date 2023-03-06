from celery import shared_task
from django.core.mail import send_mail

from fundoonotes import settings


@shared_task(bind=True)
def send_mail_func(self, subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return "done"
