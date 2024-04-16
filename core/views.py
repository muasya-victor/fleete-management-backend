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
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db import transaction
import os
from rest_framework import generics
from django.conf import settings

import requests
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from core.models import( User, VehicleService, ServiceType, SubService, VehiclePart, Vehicle)
from core.serializers import ( CustomTokenObtainPairSerializer, UserSerializer,SubServiceSerializer,
                ServiceTypeSerializer, VehiclePartSerializer, VehicleServiceSerializer, VehicleSerializer)

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
    

class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
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

class VehicleServiceViewSet(viewsets.ModelViewSet):
    serializer_class= VehicleServiceSerializer
    queryset = VehicleService.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        user = self.request.user
        if user.user_type == "mechanic" and not user.is_superuser:
            return Vehicle.objects.filter(mechanic=user)
        elif user.is_superuser:
            return Vehicle.objects.all()
        else:
            # Return an empty queryset for non-mechanics who are not superusers
            return Vehicle.objects.none()
        
class GeneratePDF(APIView):
    def get(self, request):
        # Create an in-memory PDF file
        buffer = BytesIO()

        # Set up the PDF document
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Fetch vehicle data using VehicleSerializer
        vehicles = Vehicle.objects.all()
        vehicle_serializer = VehicleSerializer(vehicles, many=True)

        # Create tables to display the serialized data
        vehicle_data = [[ 'Plate Number',
                         'Vehicle Status', 'Type', 'Model', 'Engine Number', 'Color']]
        for vehicle_data_item in vehicle_serializer.data:
            vehicle_data.append([
                vehicle_data_item['vehicle_plate_number'],
                vehicle_data_item['vehicle_general_condition'],
                vehicle_data_item['vehicle_type'],
                vehicle_data_item['vehicle_model'],
                vehicle_data_item['vehicle_engine_number'],
                vehicle_data_item['vehicle_color']
            ])

        vehicle_table = Table(vehicle_data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('TABLEWIDTH', (0, 0), (-1, -1), '100%'),
        ])

        vehicle_table.setStyle(style)
        elements.append(vehicle_table)

        # Build the PDF document
        pdf.build(elements)
        buffer.seek(0)

        # Send the PDF as a response
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="vehicle_details.pdf"'

        return response