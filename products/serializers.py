from rest_framework import serializers

from . import models


# class CategorySerializer(serializers.ModelSerializer):
#     parent_category = CategorySerializer(many=False)
#
#     class Meta:
#         model = models.Category
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
