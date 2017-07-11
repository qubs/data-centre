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


import datetime
import dateutil.parser
import pytz

from collections import OrderedDict

from django.db.models import Q

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from climate_data.serializers import *


compact_reading_columns = ("id", "read_time", "value", "invalid", "sensor", "station")
station_compact_reading_columns = ("id", "read_time", "value", "invalid", "sensor")


# API Root View

@api_view(["GET"])
def climate_api_root(request, format=None):
    return Response(OrderedDict([
        ("data-types", reverse("data-type-list", request=request, format=format)),
        ("sensors", reverse("sensor-list", request=request, format=format)),
        ("stations", reverse("station-list", request=request, format=format)),
        ("station-sensor-links", reverse("station-sensor-link-list", request=request, format=format)),
        ("readings", reverse("reading-list", request=request, format=format)),
        ("latest-readings", reverse("reading-latest", request=request, format=format)),
        ("messages", reverse("message-list", request=request, format=format)),
        ("latest-messages", reverse("message-latest", request=request, format=format)),
        ("settings", reverse("setting-list", request=request, format=format)),
    ]))


# Data Type Views

class DataTypeList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all data types.
    
    post:
    Create a new data type in the database.
    """

    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DataTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return information about a given data type.
    
    put:
    Update a given data type with new information.
    """

    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# Sensor Views

class SensorList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all sensors.
    
    post:
    Create a new sensor in the database.
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return information about a given sensor.
    
    put:
    Update a given sensor with new information.
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SensorData(generics.ListAPIView):
    """
    get:
    Return readings associated with a particular sensor.
    """

    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Reading.objects.filter(sensor=pk)


class SensorStations(generics.ListAPIView):
    """
    Return stations which are linked with a given sensor.
    """

    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]

        return Station.objects.filter(
            sensors__id=pk
        )


# Station Views

class StationList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all stations, or optionally any (almost always just one) station with a particular GOES ID.
    
    post:
    Create a new station in the database.
    """

    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Station.objects.all()

        goes_id = self.request.query_params.get("goes_id", None)
        if goes_id is not None:
            queryset = queryset.filter(goes_id=goes_id)

        return queryset


class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Return information about a given station.
    """

    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StationData(generics.ListAPIView):
    """
    Return a list of readings associated with a given station.
    """

    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]

        start_date = self.request.query_params.get("start", None)
        start_date_object = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)  # Default to a week's worth
        if start_date is not None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get("end", None)
        end_date_object = datetime.datetime.now(pytz.utc)
        if end_date is not None:
            end_date_object = dateutil.parser.parse(end_date)

        return_compact = self.request.query_params.get("compact", False)

        queryset = Reading.objects.filter(
            station=pk,
            read_time__gte=start_date_object,
            read_time__lte=end_date_object
        )

        if return_compact == "true":
            self.serializer_class = StationCompactReadingSerializer
            queryset = queryset.only(*station_compact_reading_columns)

        return queryset


class StationLatestData(generics.ListAPIView):
    """
    Return a list of the latest readings (taken in the past hour) associated with a given station.
    """

    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        latest_message = Message.objects.filter(station=pk).latest("arrival_time")
        start_date_object = latest_message.arrival_time - datetime.timedelta(hours=1)

        return_compact = self.request.query_params.get("compact", False)

        queryset = Reading.objects.filter(
            station=pk,
            read_time__gte=start_date_object,
        )

        if return_compact == "true":
            self.serializer_class = StationCompactReadingSerializer
            queryset = queryset.only(*station_compact_reading_columns)

        return queryset


class StationSensors(generics.ListAPIView):
    """
    Return a list of sensors associated with a given station.
    """

    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Sensor.objects.filter(stations__id=pk).order_by("stationsensorlink__station_order")


class StationSensorLinks(generics.ListAPIView):
    """
    Return a list of station-sensor links associated with a given station.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        deep = str(self.request.query_params.get("deep", "false")).lower()

        if deep == "false" or deep == "0":
            return StationSensorLinkSerializer

        return DeepStationSensorLinkSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = StationSensorLink.objects.filter(station_id=pk).order_by("station_order")

        return queryset


class StationMessages(generics.ListAPIView):
    """
    Return a list of messages associated with a given station.
    """

    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Message.objects.filter(station=pk).order_by("arrival_time")


class StationLatestMessage(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        pk = self.kwargs["pk"]
        return self.queryset.filter(station_id=pk).latest("arrival_time")


# Station-Sensor Link Views

class StationSensorLinkList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        deep = str(self.request.query_params.get("deep", "false")).lower()

        if deep == "false" or deep == "0":
            return StationSensorLinkSerializer

        return DeepStationSensorLinkSerializer

    def get_queryset(self):
        station = self.request.query_params.get("station", None)
        sensor = self.request.query_params.get("sensor", None)

        queryset = StationSensorLink.objects.all().order_by("created")

        if station:
            try:
                station = int(station)
            except ValueError:
                pass  # There was a value error, so no filtering will be applied.
            else:
                queryset = queryset.filter(station=station)

        if sensor:
            try:
                sensor = int(sensor)
            except ValueError:
                pass  # There was a value error, so no filtering will be applied.
            else:
                queryset = queryset.filter(sensor=sensor)

        return queryset


class StationSensorLinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StationSensorLink.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        deep = str(self.request.query_params.get("deep", "false")).lower()

        if deep == "false" or deep == "0":
            return StationSensorLinkSerializer

        return DeepStationSensorLinkSerializer


# Reading Views

class ReadingList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        compact = str(self.request.query_params.get("compact", "false")).lower()

        if compact == "false" or compact == "0":
            return ReadingSerializer

        return CompactReadingSerializer

    def get_queryset(self):
        global compact_reading_columns

        start_date = self.request.query_params.get("start", None)
        start_date_object = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)  # Default to a week's worth
        if start_date is not None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get("end", None)
        end_date_object = datetime.datetime.now(pytz.utc)
        if end_date is not None:
            end_date_object = dateutil.parser.parse(end_date)

        sample_interval = self.request.query_params.get("interval", "1")  # TODO: Make this more elegant.

        try:
            sample_interval = int(sample_interval)
        except ValueError:
            sample_interval = 1

        start_exclusive = self.request.query_params.get("start_exclusive", False)
        sensors = self.request.query_params.getlist("sensors[]")

        queryset_filter = {
            'read_time__gte': start_date_object,
            'read_time__lte': end_date_object
        }

        if start_exclusive == "true":
            queryset_filter = {
                'read_time__gt': start_date_object,
                'read_time__lte': end_date_object
            }

        queryset = Reading.objects.only(*compact_reading_columns).filter(**queryset_filter)

        if sample_interval == 2:
            queryset = queryset.filter(Q(read_time__contains=":00:") | Q(read_time__contains=":30:"))

        if sample_interval == 4:
            queryset = queryset.filter(read_time__contains=":00:")

        if sample_interval == 96:  # TODO: This should probably retrieve an average from a cache - more robust.
            queryset = queryset.filter(read_time__contains="00:00:")

        if sensors:
            queryset = queryset.filter(sensor__in=sensors)

        queryset = queryset.order_by("read_time")
        return queryset


class ReadingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReadingLatest(generics.ListAPIView):
    serializer_class = CompactReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        stations = Station.objects.all()
        station_ids = []
        for s in stations:
            station_ids.append(s.id)

        latest_message = Message.objects.latest("arrival_time")
        start_date_object = latest_message.arrival_time - datetime.timedelta(hours=1)

        return Reading.objects.filter(
            station__in=station_ids,
            read_time__gte=start_date_object,
        )


# Message Views

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        print("--- CREATING MESSAGE ---")
        print(self.request.data)
        print("------------------------")
        serializer.save()

    def get_queryset(self):
        start_date = self.request.query_params.get("start", None)
        start_date_object = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)  # Default to a week's worth
        if start_date is not None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get("end", None)
        end_date_object = datetime.datetime.now(pytz.utc)
        if end_date is not None:
            end_date_object = dateutil.parser.parse(end_date)

        start_exclusive = self.request.query_params.get("start_exclusive", False)
        goes_id = self.request.query_params.get("goes_id", None)

        queryset_filter = {
            'arrival_time__gte': start_date_object,
            'arrival_time__lte': end_date_object
        }

        if start_exclusive == "true":
            queryset_filter = {
                'arrival_time__gt': start_date_object,
                'arrival_time__lte': end_date_object
            }

        if goes_id is not None:
            queryset_filter['goes_id'] = goes_id

        queryset = Message.objects.filter(**queryset_filter).order_by("arrival_time")

        return queryset


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MessageLatest(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        latest_message = Message.objects.latest("arrival_time")
        start_date_object = latest_message.arrival_time - datetime.timedelta(hours=1)

        return Message.objects.filter(
            arrival_time__gte=start_date_object
        )


class SettingList(generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SettingDetail(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SettingDetailWithName(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        name = self.kwargs["name"]
        return self.queryset.filter(name=name).first()
