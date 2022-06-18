import required
from django.db.models import Q, F
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.viewsets import generics

from . import models
from . import serializers
from config import settings
from django_filters import rest_framework as filters
from rest_framework import filters as sFilters


class SearchResultsView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    model = models.Product
    serializer_class = serializers.ProductSerializer
    filter_backends = [sFilters.SearchFilter]
    search_fields = ['name', 'description', 'manufacturer', 'category__name']

class FilterProducts(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_favorites_count = filters.NumberFilter(field_name="favorites_count", lookup_expr='gte')
    max_favorites_count = filters.NumberFilter(field_name="favorites_count", lookup_expr='lte')
    location = filters.BaseInFilter(field_name="location", lookup_expr='in')
    manufacturer = filters.BaseInFilter(field_name="manufacturer", lookup_expr='in')
    category = filters.BaseInFilter(field_name="category__name", lookup_expr='in')
    parent_product = filters.BaseInFilter(field_name="parent_product__name", lookup_expr='in')

    class Meta:
        model = models.Product
        fields = ['min_price', 'max_price', 'min_favorites_count', 'max_favorites_count',
                  'manufacturer', 'location', 'category', 'parent_product']

class FilterResultsView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    model = models.Product
    serializer_class = serializers.ShortProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FilterProducts


    def get_queryset(self):
        serializer = serializers.SearchingSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        query_list = models.ValueAsset.objects.all().values_list('product__id', flat=True)
        try:
            filters = serializer.validated_data['filters']
            if filters:
                for f in filters:
                    filter_list = (Q(**{'asset__name': f['filterBy']}) & Q(**{'value': f['filterType']}))
                    object_list = list(models.ValueAsset.objects.filter(filter_list).values_list('product__id', flat=True))
                    query_list = [x for x in object_list if x in query_list]
                return models.Product.objects.filter(id__in=query_list)
        except:
            pass
        return models.Product.objects.all()


class ListFavoriteAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Favorites.objects.filter(user=user)


class CreateFavoriteAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Favorites.objects.all()
    serializer_class = serializers.FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFavoriteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Favorites.objects.all()
    serializer_class = serializers.FavoriteSerializer


class CreateProductAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProductCardSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if update_or_create_product(serializer, request.user):
            return Response(data=request.data, status=status.HTTP_201_CREATED)


class UpdateProductAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ShortProductSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if update_or_create_product(serializer, request.user, self.request.query_params.get('id')):
            return Response(data=request.data, status=status.HTTP_201_CREATED)


def update_or_create_assets(assets, product):
    for k, value in assets.items():
        asset = models.Asset.objects.filter(slug=k).first()
        models.ValueAsset.objects.update_or_create(
            product=product,
            asset=asset,
            defaults={
                "asset": asset,
                "value": value,
                "product": product
            }
        )

def update_or_create_product(serializer, user, id=None):
    try:
        product, created = models.Product.objects.update_or_create(
            id=id,
            defaults={
                "user": user,
                "manufacturer": serializer.validated_data['manufacturer'],
                "name": serializer.validated_data['name'],
                "price": serializer.validated_data['price'],
                "description": serializer.validated_data['description'],
                "category": serializer.validated_data['category'],
                "parent_product": serializer.validated_data['parent_product'],
                "location": serializer.validated_data['location'],
            }
        )
        if 'assets' in serializer.validated_data:
            update_or_create_assets(serializer.validated_data['assets'], product)
        return True
    except:
        return Response('Error in creating/updating product', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteProductAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ListProductsAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ShortProductSerializer
    queryset = models.Product.objects.all()


class DetailProductAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DetailProductsSerializer
    queryset = models.Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history = models.History(product=instance, user=request.user)
        history.save()
        return Response(serializer.data)


class GetAssetTemplate(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AssetTemplateSerializer

    def get_queryset(self):
        cat = models.Category.objects.get(id=self.kwargs['category_id'])
        return models.AssetTemplate.objects.filter(category=cat)


class GetCategories(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class AddPhotoAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AddingPhotoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_photo = models.Photo(
            file=serializer.validated_data['file'].replace(settings.MEDIA_ROOT+'/', ''),
            product=serializer.validated_data['product'],
        )
        new_photo.save()
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)

class DeletePhotoAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Photo.objects.all()
    serializer_class = serializers.PhotoSerializer


