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

from core.serializers import *


@api_view(["GET"])
def api_root(request, format=None):
    return Response(OrderedDict([
        ("sensors", reverse("sensor-list", request=request, format=format)),
        ("stations", reverse("station-list", request=request, format=format)),
        ("station-sensor-links", reverse("station-sensor-link-list", request=request, format=format)),
        ("readings", reverse("reading-list", request=request, format=format)),
        ("latest-readings", reverse("reading-latest", request=request, format=format)),
        ("messages", reverse("message-list", request=request, format=format)),
        ("latest-messages", reverse("message-latest", request=request, format=format)),
        ("settings", reverse("setting-list", request=request, format=format)),
        ("users", reverse("user-list", request=request, format=format)),
    ]))


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class SensorData(generics.ListAPIView):
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Reading.objects.filter(sensor=pk)

class SensorStations(generics.ListAPIView):
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]

        return Station.objects.filter(
            sensors__id=pk
        )


class StationList(generics.ListCreateAPIView):
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Station.objects.all()

        goes_id = self.request.query_params.get("goes_id", None)
        if goes_id is not None:
            queryset = Station.objects.filter(goes_id=goes_id)

        return queryset

class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class StationData(generics.ListAPIView):
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]

        start_date = self.request.query_params.get("start", None)
        start_date_object = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7) # Default to a week's worth
        if start_date is not None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get("end", None)
        end_date_object = datetime.datetime.now(pytz.utc)
        if end_date is not None:
            end_date_object = dateutil.parser.parse(end_date)

        return Reading.objects.filter(
            station=pk,
            read_time__gte=start_date_object,
            read_time__lte=end_date_object
        )

class StationLatestData(generics.ListAPIView):
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        latest_message = Message.objects.filter(station=pk).latest("arrival_time")
        start_date_object = latest_message.arrival_time - datetime.timedelta(hours=1)

        return Reading.objects.filter(
            station=pk,
            read_time__gte = start_date_object,
        )

class StationSensors(generics.ListAPIView):
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Sensor.objects.filter(stations__id=pk).order_by("stationsensorlink__station_order")

class StationMessages(generics.ListAPIView):
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


class StationSensorLinkList(generics.ListCreateAPIView):
    queryset = StationSensorLink.objects.all().order_by("created")
    serializer_class = StationSensorLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class StationSensorLinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StationSensorLink.objects.all()
    serializer_class = StationSensorLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReadingList(generics.ListCreateAPIView):
    serializer_class = CompactReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
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

        queryset = Reading.objects.filter(
            read_time__gte=start_date_object,
            read_time__lte=end_date_object
        )

        if start_exclusive == "true":
            queryset = Reading.objects.filter(
                read_time__gt=start_date_object,
                read_time__lte=end_date_object
            )

        if sample_interval == 2:
            queryset = queryset.filter(Q(read_time__contains=":00:") | Q(read_time__contains=":30:"))

        if sample_interval == 4:
            queryset = queryset.filter(read_time__contains=":00:")

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

        latest_message = Message.objects.all().latest("arrival_time")
        start_date_object = latest_message.arrival_time - datetime.timedelta(hours=1)

        return Reading.objects.filter(
            station__in=station_ids,
            read_time__gte=start_date_object,
        )


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

        queryset = Message.objects.filter(
            arrival_time__gte=start_date_object,
            arrival_time__lte=end_date_object
        )

        if start_exclusive == "true":
            queryset = Message.objects.filter(
                arrival_time__gt=start_date_object,
                arrival_time__lte=end_date_object
            )

        queryset = queryset.order_by("arrival_time")

        goes_id = self.request.query_params.get("goes_id", None)
        if goes_id is not None:
            queryset = Message.objects.filter(
                arrival_time__gte=start_date_object,
                arrival_time__lte=end_date_object,

                goes_id=goes_id
            ).order_by("arrival_time")

        return queryset

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class MessageLatest(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        latest_message = Message.objects.all().latest("arrival_time")
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
