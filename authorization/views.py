from clients.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# Create your views here.
from rest_framework import generics, status, permissions

from authorization import models
from authorization.serializers import ConfirmMailSerializer, CheckMailSerializer, SendCodeSerializer
from services.mail import check_mail, send_mail_code, success_verify_email


class SendCodeView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']
        if login is None:
            return JsonResponse(
                dict(
                    message='Bad request. Enter your phone login'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            try:
                user = User.objects.get(email__icontains=login)
                send_mail_code(user)
                return JsonResponse(
                    dict(
                        message=f'User {user.id} found',
                        email=user.email
                    ),
                    status=status.HTTP_200_OK
                )

            except ObjectDoesNotExist:
                return JsonResponse(
                    dict(
                        message=f'User not found'
                    ),
                    status=status.HTTP_404_NOT_FOUND
                )

class CheckMail(generics.GenericAPIView):
    serializer_class = CheckMailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail = serializer.validated_data['mail']
        try:
            user = User.objects.get(email=mail)
            return JsonResponse(dict(
                message=f'Existed'
            ),
                status=status.HTTP_202_ACCEPTED
            )
        except ObjectDoesNotExist:
            check_mail(mail=mail)
            return JsonResponse(dict(
                message=f'Message sended'
            ),
                status=status.HTTP_200_OK
            )


class ConfirmMail(generics.GenericAPIView):
    serializer_class = ConfirmMailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail = serializer.validated_data['mail']
        code = serializer.validated_data['code']
        try:
            verify = models.Mail_verification.objects.get(mail=mail, code=code)
            new_user = User(email=mail)
            new_user.set_password(str(code))
            new_user.save()
            success_verify_email(mail)
            return JsonResponse(dict(
                message='Mail confirmed'
            ),
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return JsonResponse(dict(
                message='Mail not exist'
            ),
                status=status.HTTP_404_NOT_FOUND
            )
