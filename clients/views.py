from rest_framework import permissions
from rest_framework.viewsets import generics

from . import serializers
# Create your views here.
from .models import User, Review


class UpdateUserView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class ListUserView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class GetDetailUserView(generics.RetrieveAPIView):
    serializer_class = serializers.GetDetailUserSerializer
    queryset = User.objects.all()


class CreateReviewView(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
