from rest_framework import serializers
from .models import Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для измерений"""
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'temperature', 'created_at', 'photo']

class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для списка датчиков (краткая информация)"""
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о датчике (с измерениями)"""
    
    measurements = MeasurementSerializer(read_only=True, many=True)
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements', 'created_at', 'updated_at']