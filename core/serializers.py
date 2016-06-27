from rest_framework import serializers
from core.models import Sensor, Station, Reading

class SensorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sensor
		fields = ("id", "created", "updated", "name", "data_id", "decimals")

class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Station
		fields = ("id", "created", "updated", "name", "goes_id", "sensors")

class ReadingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reading
		fields = ("id", "created", "updated", "read_time", "value", "sensor", "station")
