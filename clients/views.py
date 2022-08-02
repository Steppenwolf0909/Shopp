from rest_framework import permissions
from rest_framework.viewsets import generics

from . import serializers
# Create your views here.
from .models import User, Review
from products.models import Product
from products.serializers import ShortProductWithStatusSerializer


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
        return Product.objects.filter(user_id=self.kwargs['pk'])



class CreateReviewView(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
