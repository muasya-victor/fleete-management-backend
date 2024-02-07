from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import CustomObtainTokenPairView ,UserViewSet, ServiceTypeViewSet , SubServiceViewSet

core_router = DefaultRouter()
core_router.register(r"user", UserViewSet)
core_router.register(r"service-type", ServiceTypeViewSet)
core_router.register(r"sub-service", SubServiceViewSet)

url_patterns = core_router.urls
url_patterns += [
    path("token/request/", CustomObtainTokenPairView.as_view(), name="token_request"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   

]