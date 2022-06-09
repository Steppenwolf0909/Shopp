from rest_framework import serializers

from . import models


# class CategorySerializer(serializers.ModelSerializer):
#     parent_category = CategorySerializer(many=False)
#
#     class Meta:
#         model = models.Category
#         fields = '__all__'
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorites
        fields = '__all__'

class ShortProductSerializer(serializers.ModelSerializer):
    photo = serializers.CharField()

    class Meta:
        model = Product
        fields = ['name', 'manufacturer', 'price', 'location', 'photo']



class DetailProductsSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email')
    user_avatar = serializers.CharField(source='user.avatar')

    class Meta:
        model = Product
        exclude = ("user",)
        extra_fields = ('user_email', 'user_avatar')


