import random

from django.http import JsonResponse
from rest_framework import status

from authorization import models
from services.celery import send_async_db_mail


def send_mail_code(user):
    try:
        code = random.randint(1000, 9999)
        user.set_password(str(code))
        user.save()
        send_async_db_mail.delay('code', user.email, {'code': code})
    except Exception:
        return JsonResponse(
            dict(
                message='Error, Message not sent'
            ),
            status=status.HTTP_400_BAD_REQUEST
        )


def check_mail(mail):
    try:
        code = random.randint(1000, 9999)
        new_verify = models.Mail_verification(code=code, mail=mail)
        new_verify.save()
        send_async_db_mail.delay('code', mail, {'code': code})
    except Exception:
        return JsonResponse(
            dict(
                message='Error, Message not sent'
            ),
            status=status.HTTP_400_BAD_REQUEST
        )


def success_verify_email(email):
    try:
        send_async_db_mail.delay('success-email-verify', email, {'text': 'Your mail successfully verified'})
    except Exception:
        return JsonResponse(
            dict(
                message='Error, Message not sent'
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
