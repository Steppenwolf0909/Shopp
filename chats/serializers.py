from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError

from chats.models import Message, BusinessChat
from streamers.models import Streamer
from company.models import Company, CompanyEmployee


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    streamer_id = serializers.SerializerMethodField(method_name='get_streamer')
    employee_id = serializers.SerializerMethodField(method_name='get_employee_id')
    employee_email = serializers.SerializerMethodField(method_name='get_employee_email')

    class Meta:
        model = Message
        fields = (
            'uid', 'author', 'text', 'created_at', 'file',
            'video_preview', 'file_size', 'is_read', 'streamer_id', 'employee_id', 'employee_email'
        )
        read_only_fields = ['streamer_id', 'employee_id', 'employee_email']

    @staticmethod
    def get_streamer(message):
        streamer_id = Streamer.objects.filter(user_id=message.author.id)
        if streamer_id:
            return streamer_id.first().id
        return None

    @staticmethod
    def get_employee_id(message):
        employee_id = CompanyEmployee.objects.filter(user_id=message.author.id)
        if employee_id:
            return employee_id.first().id
        return None

    @staticmethod
    def get_employee_email(message):
        employee_id = CompanyEmployee.objects.filter(user_id=message.author.id)
        if employee_id:
            return employee_id.first().email
        return None


class BusinessChatSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(source='get_last_message')
    unread_messages_count = serializers.IntegerField()
    business_name = serializers.SerializerMethodField(method_name='get_business_name')
    business_logo = serializers.SerializerMethodField(method_name='get_business_logo')
    streamer_username = serializers.SerializerMethodField(method_name='get_streamer_username')
    streamer_avatar = serializers.SerializerMethodField(method_name='get_streamer_avatar')
    employee = serializers.SerializerMethodField(method_name='get_employee')

    class Meta:
        model = BusinessChat
        fields = (
            'uid', 'business', 'client', 'unread_messages_count', 'last_message', 'business_name', 'business_logo',
            'streamer_username', 'streamer_avatar', 'employee'
        )
        read_only_fields = (
            'uid', 'last_message', 'business_name', 'business_logo', 'streamer_username', 'streamer_avatar',
            'employee'
        )

    @staticmethod
    def get_business_name(chat):
        if chat.business:
            company = Company.objects.filter(id=chat.business.id)
            if company:
                return company.first().title
            return ""
        return ""

    @staticmethod
    def get_business_logo(chat):
        if chat.business:
            company = Company.objects.filter(id=chat.business.id)
            if company:
                return company.first().image.url
            return ""
        return ""

    @staticmethod
    def get_streamer_username(chat):
        if chat.client:
            streamer = Streamer.objects.filter(user_id=chat.client.id)
            if streamer:
                return streamer.first().username
            return ""
        return ""

    @staticmethod
    def get_employee(chat):
        if chat.client:
            company_employee = CompanyEmployee.objects.filter(user_id=chat.client.id)
            if company_employee:
                company_employee = company_employee.first()
                return {
                    'company': f'{company_employee.company}',
                    'email': f'{company_employee.email}',
                    'avatar': f'{company_employee.company.image.url}'
                }
            return ""
        return ""

    @staticmethod
    def get_streamer_avatar(chat):
        if chat.client:
            streamer = Streamer.objects.filter(user_id=chat.client.id)
            if streamer:
                return streamer.first().avatar.url
            return ""
        return ""


class BusinessChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessChat
        fields = ('uid', 'business', 'client')
        extra_kwargs = {
            'business': {'required': True},
            'client': {'required': True},
        }

    def validate(self, attrs):
        if not hasattr(attrs['business'], 'business_profile'):
            raise ValidationError({'business': 'User have not business_profile'})
        if not hasattr(attrs['client'], 'client'):
            raise ValidationError({'client': 'User have not client'})
        return attrs