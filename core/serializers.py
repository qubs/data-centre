from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Sensor, Station, Reading, Message

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

class MessageSerializer(serializers.ModelSerializer):
    values = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Message
        fields = ("id", "created", "updated", "goes_id", "goes_channel", "goes_spacecraft",
            "arrival_time", "failure_code", "signal_strength", "frequency_offset", "modulation_index",
            "data_quality", "data_source", "recorded_message_length", "values", "message_text", "station")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
