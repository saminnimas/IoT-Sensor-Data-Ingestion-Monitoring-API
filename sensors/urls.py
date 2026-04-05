from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, SensorReadingViewSet


router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'readings', SensorReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]