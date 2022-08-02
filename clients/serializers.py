from rest_framework import serializers

from clients.models import Review, User
from products.models import Product


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'groups', 'user_permissions', 'is_superuser')


