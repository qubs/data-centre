# Copyright 2016 the Queen's University Biological Station

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Sensor, Station, StationSensorLink, Reading, Message


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ("id", "created", "updated", "name", "data_id", "decimals")


class StationSerializer(serializers.ModelSerializer):
    sensors = serializers.SerializerMethodField("get_sensor_list")

    def get_sensor_list(self, instance):
        return StationSensorLink.objects.filter(station = instance.id).order_by("station_order").values_list("sensor_id", flat=True)

    class Meta:
        model = Station
        fields = ("id", "created", "updated", "name", "goes_id", "sensors")

class StationSensorLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationSensorLink
        fields = ("id", "created", "updated", "station", "sensor", "station_order", "read_frequency")


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
