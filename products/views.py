from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.viewsets import generics

from . import models
from . import serializers


class SearchResultsView(generics.ListAPIView):
    model = models.Product
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        sortBy = self.request.GET.get('sortBy')
        filterBy = self.request.GET.get('filterBy')
        filterType = self.request.GET.get('filterType')
        if query:
            regularExp = r'.*([а-яА-Я]+)*%s([а-яА-Я]+)*.*'
            object_list = models.Product.objects.filter(Q(name__iregex=regularExp % query) |
                                                        Q(description__iregex=regularExp % query) |
                                                        Q(manufacturer__iregex=regularExp % query) |
                                                        Q(category__name__iregex=regularExp % query)
                                                        )
            return object_list
        if sortBy:
            object_list = models.Product.objects.order_by(sortBy)
            return object_list
        if (filterBy and filterType):
            object_list = models.Product.objects.filter(**{filterBy: filterType})
            return object_list
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
        new_product = models.Product(
            user=request.user,
            category=serializer.validated_data['category'],
            manufacturer=serializer.validated_data['manufacturer'],
            name=serializer.validated_data['name'],
            price=serializer.validated_data['price'],
            description=serializer.validated_data['description'],
            location=serializer.validated_data['location'],
        )
        if 'parent_product' in serializer.validated_data:
            new_product.parent_product = serializer.validated_data['parent_product']
        new_product.save()
        update_or_create_assets(assets=serializer.validated_data['assets'], product=new_product)
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)

class UpdateProductAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def patch(self, serializer):
        update_or_create_assets(self.request, self.request.query_params.get('id'))
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)


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
            file=serializer.validated_data['file'],
            product=serializer.validated_data['product'],
        )
        new_photo.save()
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)

class DeletePhotoAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Photo.objects.all()
    serializer_class = serializers.PhotoSerializer