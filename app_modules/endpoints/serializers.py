from rest_framework import serializers

from .models import WeatherLog


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherLog
        fields = '__all__'
