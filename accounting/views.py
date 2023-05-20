from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from constants.statics import SimpleViewSet

from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer, UserProfileCreateSerializer


class UserViewSet(SimpleViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    list_filtering = {"username" : "username__icontains", "email" : "email__icontains", "is_active" : "is_active", "is_staff" : "is_staff"}


class UserProfileViewSet(SimpleViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    create_serializer_class = UserProfileCreateSerializer
    list_filtering = {"bio" : "bio__icontains"}
    
    
