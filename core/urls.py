from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import (CustomObtainTokenPairView ,UserViewSet, ServiceTypeViewSet ,CurrentUserViewSet,
                        SubServiceViewSet, VehiclePartViewSet,VehicleServiceViewSet, VehicleViewSet, GeneratePDF)

core_router = DefaultRouter()
core_router.register(r"user", UserViewSet)
core_router.register(r"service-type", ServiceTypeViewSet)
core_router.register(r"sub-service", SubServiceViewSet)
core_router.register(r"vehicle-part", VehiclePartViewSet)
core_router.register(r"vehicle-service", VehicleServiceViewSet)
core_router.register(r"vehicle", VehicleViewSet)
core_router.register(r"current-user", CurrentUserViewSet, basename='current_user')

url_patterns = core_router.urls
url_patterns += [
    path("token/request/", CustomObtainTokenPairView.as_view(), name="token_request"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('pdf-report/', GeneratePDF.as_view(), name='generate_pdf')
   
]