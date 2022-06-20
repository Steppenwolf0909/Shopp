from django_filters import rest_framework as filters
from . import models

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