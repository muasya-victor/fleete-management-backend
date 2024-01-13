import calendar

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
from core.models import( VehicleService)
from core.seriazilers import ( CustomTokenObtainPairSerializer)

class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer