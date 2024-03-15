import calendar
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from django.db import transaction
import os
from rest_framework import generics
from django.conf import settings

import requests
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from core.models import( User, VehicleService, ServiceType, SubService, VehiclePart)
from core.serializers import ( CustomTokenObtainPairSerializer, UserSerializer,SubServiceSerializer,
                              ServiceTypeSerializer, VehiclePartSerializer)

class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer



class UserViewSet(viewsets.ModelViewSet):
    serializer_class =UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            user = User.objects.filter(user=user)
        else:
            user = User.objects.all()
        return user
    
class ServiceTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceTypeSerializer
    queryset = ServiceType.objects.all()
    permission_classes =[permissions.IsAuthenticated]


class SubServiceViewSet(viewsets.ModelViewSet):
    serializer_class = SubServiceSerializer
    queryset = SubService.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class VehiclePartViewSet(viewsets.ModelViewSet):
    serializer_class =VehiclePartSerializer
    queryset = VehiclePart.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        user = self.request.user
        if user.user_type == "mechanic" and not user.is_superuser:
            return VehiclePart.objects.filter(mechanic=user)
        elif user.is_superuser:
            return VehiclePart.objects.all()
        else:
            # Return an empty queryset for non-mechanics who are not superusers
            return VehiclePart.objects.none()