
from rest_framework.generics import ListAPIView
from django.db.models import Q
from products.models import Product
from products.serializers import ProductSerializer


class SearchResultsView(ListAPIView):
    model = Product
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        sortBy = self.request.GET.get('sortBy')
        filterBy = self.request.GET.get('filterBy')
        filterType = self.request.GET.get('filterType')
        if query:
            regularExp=r'.*([а-яА-Я]+)*%s([а-яА-Я]+)*.*'
            object_list = Product.objects.filter(Q(name__iregex=regularExp % query) |
                                                 Q(description__iregex=regularExp % query) |
                                                 Q(manufacturer__iregex=regularExp % query) |
                                                 Q(category__name__iregex=regularExp % query)
                                                 )
            return object_list
        if sortBy:
            object_list = Product.objects.order_by(sortBy)
            return object_list
        if (filterBy and filterType):
            object_list = Product.objects.filter(**{filterBy: filterType})
            return object_list
        return Product.objects.all()



