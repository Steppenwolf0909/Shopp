from django.db.models import Q
from rest_framework import permissions
from rest_framework.viewsets import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status
from clients import models as clients_models


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

class CreateProductAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def post(self, serializer):
        update_or_create_product(self.request)
        # category = models.Category.objects.filter(id=self.request.data.get("category")).first()
        # parent_product = models.Product.objects.filter(id=self.request.data.get("parent_product")).first()
        # assets = self.request.data.get('assets')
        # product = models.Product.objects.create(
        #     user=self.request.user,
        #     manufacturer=self.request.data.get("manufacturer"),
        #     name=self.request.data.get("name"),
        #     price=self.request.data.get("price"),
        #     description=self.request.data.get("description"),
        #     category=category,
        #     parent_product=parent_product,
        #     location=self.request.data.get("location"),
        # )
        # for k, value in assets.items():
        #     asset = models.Asset.objects.filter(name=k).first()
        #     models.ValueAsset.objects.create(
        #         asset=asset,
        #         value=value,
        #         product=product
        #     )
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)

class DeleteProductAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

class UpdateProductAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def post(self, serializer):
        update_or_create_product(self.request, self.request.query_params.get('id'))
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)


def update_or_create_product(request, id=None):
    category = models.Category.objects.filter(id=request.data.get("category")).first()
    parent_product = models.Product.objects.filter(id=request.data.get("parent_product")).first()
    assets = request.data.get('assets')
    product, created = models.Product.objects.update_or_create(
        id=id,
        defaults={
            "user": request.user,
            "manufacturer": request.data.get("manufacturer"),
            "name": request.data.get("name"),
            "price": request.data.get("price"),
            "description": request.data.get("description"),
            "category": category,
            "parent_product": parent_product,
            "location": request.data.get("location"),
        }
    )
    for k, value in assets.items():
        asset = models.Asset.objects.filter(name=k).first()
        models.ValueAsset.objects.update_or_create(
            product__id=product.id,
            asset__id=asset.id,
            defaults={
                "asset": asset,
                "value": value,
                "product": product
            }
        )
    return 1

# class ListProductsAPIView(generics.ListAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = serializers.ShortProductSerializer
#
#     def get_queryset(self):
#         products = models.Product.objects.all()
#         prods = []
#         for pr in products:
#             image = models.Photo.objects.filter(product__id=pr.id).first()
#             prods.append({"image": image.image, "product": pr})
#         return prods