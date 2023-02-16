from celery import shared_task
from django.core.mail import send_mail
from fundoonotes import settings

#
#
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



#
# @shared_task(blind=True)
# def send_mail_func():
#     users = get_user_model().objects.all()  #i want to send mail to all user
#     # timezone.localtime(users.date_time)
#     for user in users:
#         mail_subject = "hiii,celery testing"
#         message = "hello everyone Nikita is here"
#         to_email = user.email  #user to whome u want to send mail
#         print(to_email)
#         send_mail(
#             subject=mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[to_email],
#             fail_silently=True
#         )
#         return "Done"
