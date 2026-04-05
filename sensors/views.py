from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.cache import cache

from .models import Device, SensorReading
from .serializers import DeviceSerializer, SensorReadingSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # custom route: /api/devices/{id}/latest_reading/
    @action(detail=True, methods=['get'])
    def latest_reading(self, request, pk=None):
        device = self.get_object()
        cache_key = f"device_{device.id}_latest_reading"
        
        # get the data from Redis (Lightning fast)
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({"source": "Redis Cache", "data": cached_data})
            
        # If it's not in Redis, get it from PostgreSQL (Slower)
        latest_reading = device.readings.first()
        if latest_reading:
            serializer = SensorReadingSerializer(latest_reading)
            
            # Save it to Redis for next time (expires in 1 hour)
            cache.set(cache_key, serializer.data, timeout=3600)
            return Response({"source": "PostgreSQL Database", "data": serializer.data})
            
        return Response({"error": "No readings found for this device"}, status=404)
    

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    # Override the default save behavior to update the cache instantly
    def perform_create(self, serializer):
        # Save to PostgreSQL
        reading = serializer.save()
        
        # Instantly update the Redis cache for this specific device
        cache_key = f"device_{reading.device.id}_latest_reading"
        cache.set(cache_key, serializer.data, timeout=3600)