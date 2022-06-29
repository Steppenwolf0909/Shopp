import required
from rest_framework import serializers

from clients.serializers import UserSerializer
from . import models
from .models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorites
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        exclude = ('product',)


class ShortProductSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'manufacturer', 'price', 'location', 'photo')


class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = '__all__'

    def get_parent_category(self, obj):
        if obj.parent_category is not None:
            return CategorySerializer(obj.parent_category).data
        else:
            return None


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = '__all__'


class ValueAssetsSerializer(serializers.ModelSerializer):
    asset = AssetsSerializer()

    class Meta:
        model = models.ValueAsset
        fields = '__all__'


class DetailProductsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photo = PhotoSerializer(many=True)
    parent_product = ShortProductSerializer()
    category = CategorySerializer()
    assets = ValueAssetsSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCardSerializer(serializers.Serializer):
    assets = serializers.JSONField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())
    manufacturer = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=True, max_length=200)
    price = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False, max_length=2000)
    location = serializers.CharField(required=False, max_length=200)
    parent_product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), required=False)


# class AssetTemplateSerializer(serializers.ModelSerializer):
#     asset = AssetsSerializer()
#
#     class Meta:
#         model = models.AssetTemplate
#         exclude = ('category',)

class AssetTemplateSerializer(serializers.Serializer):
    asset = AssetsSerializer()
    option = serializers.JSONField(required=False)

    class Meta:
        exclude = ('category',)


class AddingPhotoSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), required=True)

    class Meta:
        model = models.Photo
        fields = '__all__'

class FilterSerializer(serializers.Serializer):
    filterBy = serializers.CharField(required=False)
    filterType = serializers.CharField(required=False)


class SearchingSerializer(serializers.Serializer):
    # sortBy = serializers.CharField(required=False)
    filters = FilterSerializer(many=True, required=False)


