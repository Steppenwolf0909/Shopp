from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from . import models
from products.serializers import ProductSerializer, FavoriteSerializer


class SearchResultsView(ListAPIView):
    model = models.Product
    serializer_class = ProductSerializer

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


class ListFavoriteAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Favorites.objects.filter(user=user)


class CreateFavoriteAPIView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Favorites.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFavoriteAPIView(DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Favorites.objects.all()
    serializer_class = FavoriteSerializer
