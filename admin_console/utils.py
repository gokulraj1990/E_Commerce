# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_custom_email(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=fail_silently,
    )