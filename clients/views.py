from rest_framework import permissions
from rest_framework.viewsets import generics

from . import serializers
# Create your views here.
from .models import User, Review
from products.models import Product
from products.serializers import ShortProductWithStatusSerializer
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UpdateUserView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class ListUserView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class GetUserProductsView(generics.ListAPIView):
    serializer_class = ShortProductWithStatusSerializer

    def get_queryset(self):
        if '%s-products' % self.kwargs['pk'] in cache:
            products = cache.get('%s-products' % self.kwargs['pk'])
            return products['data']

        else:
            products = Product.objects.filter(user_id=self.kwargs['pk'])
            data = {"data": products}
            cache.set('%s-products' % self.kwargs['pk'], data, timeout=CACHE_TTL)
            return products


class CreateReviewView(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
