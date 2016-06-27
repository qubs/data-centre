from core.models import Sensor, Station, Reading
from core.serializers import SensorSerializer, StationSerializer, ReadingSerializer
from rest_framework import mixins, generics

class SensorList(generics.ListCreateAPIView):
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer


class StationList(generics.ListCreateAPIView):
	queryset = Station.objects.all()
	serializer_class = StationSerializer

class StationDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Station.objects.all()
	serializer_class = StationSerializer


class ReadingList(generics.ListCreateAPIView):
	queryset = Reading.objects.all()
	serializer_class = ReadingSerializer

class ReadingDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Reading.objects.all()
	serializer_class = ReadingSerializer
