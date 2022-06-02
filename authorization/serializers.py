from rest_framework import serializers


class SendCodeSerializer(serializers.Serializer):
    login = serializers.EmailField(max_length=100, required=True, label='Почта')


class ConfirmMailSerializer(serializers.Serializer):
    mail = serializers.CharField(max_length=100, required=True, label='Адрес почты')
    code = serializers.CharField(max_length=4, required=True, label='Код с почты')


class CheckMailSerializer(serializers.Serializer):
    mail = serializers.CharField(max_length=100, required=True, label='Адрес почты')
