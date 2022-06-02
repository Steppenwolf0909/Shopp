from django.shortcuts import render
from rest_framework.viewsets import generics
from . import serializers
# Create your views here.
from .models import User


class UpdateUser(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()