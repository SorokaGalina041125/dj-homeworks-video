from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorView(generics.ListCreateAPIView):
    """
    GET /sensors/ - получить список всех датчиков
    POST /sensors/ - создать новый датчик
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(generics.RetrieveUpdateAPIView):
    """
    GET /sensors/{id}/ - получить детальную информацию о датчике (с измерениями)
    PATCH /sensors/{id}/ - обновить датчик
    """
    queryset = Sensor.objects.all()
    
    def get_serializer_class(self):
        # Для GET-запроса используем детальный сериализатор с измерениями
        if self.request.method == 'GET':
            return SensorDetailSerializer
        # Для PATCH/UPDATE используем обычный сериализатор
        return SensorSerializer



class MeasurementView(generics.CreateAPIView):
    """
    POST /measurements/ - создать новое измерение
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer