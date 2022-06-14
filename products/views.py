from django.db.models import Q
from rest_framework import permissions
from rest_framework.viewsets import generics
from rest_framework import views
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status




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

class CreateProductAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def post(self, serializer):
        update_or_create_product(self.request)
        return Response(data=self.request.data, status=status.HTTP_201_CREATED)

class DeleteProductAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

class UpdateProductAPIView(views.APIView):
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
    try:
        for k, value in assets.items():
            asset = models.Asset.objects.filter(name=k).first()
            models.ValueAsset.objects.update_or_create(
                product__id=id,
                asset__id=asset.id,
                defaults={
                    "asset": asset,
                    "value": value,
                    "product": product
                }
            )
    except:
        pass
    photos = request.data.get("photos")
    try:
        for ph in photos:
            models.Photo.objects.update_or_create(
                product__id=product.id,
                defaults={
                    "image": ph,
                    "product": product
                }
            )
    except:
        pass
    return 1

class ListProductsAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ShortProductSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        products = models.Product.objects.all().values()
        resp = []
        for pr in products:
            photo = models.Photo.objects.filter(product__id=pr['id']).values_list('image', flat = True).first()
            newdict = pr
            newdict.update({'photo': photo})
            resp.append(newdict)
        return resp



class DetailProductAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DetailProductsSerializer
    queryset = models.Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        photos = models.Photo.objects.filter(product__id=serializer.data.get("id")).values("image")
        newdict = serializer.data
        newdict.update({'photos': list(photos)})
        prod = models.Product.objects.filter(id=serializer.data.get("id")).first()
        history = models.History(product=prod, user=request.user)
        history.save()
        return Response(newdict)
