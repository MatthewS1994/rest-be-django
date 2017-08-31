from __future__ import unicode_literals

from rest_framework import viewsets

from .models import WeatherLog
from .serializers import WeatherSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = WeatherLog.objects.all()
    serializer_class = WeatherSerializer
