import datetime, dateutil.parser

from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.contrib.auth.models import User

from core.models import Sensor, Station, Reading, Message
from core.serializers import SensorSerializer, StationSerializer, ReadingSerializer, MessageSerializer, UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'sensors': reverse('sensor-list', request=request, format=format),
        'stations': reverse('station-list', request=request, format=format),
        'readings': reverse('reading-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


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
        pk = self.kwargs['pk']
        return Reading.objects.filter(sensor=pk)


class StationList(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class StationData(generics.ListAPIView):
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['pk']

        start_date = self.request.query_params.get('start', None)
        start_date_object = datetime.datetime.today() - datetime.timedelta(days = 7) # Default to a week's worth
        if start_date != None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get('end', None)
        end_date_object = datetime.datetime.today()
        if end_date != None:
            end_date_object = dateutil.parser.parse(end_date)

        return Reading.objects.filter(
            station = pk,
            read_time__gte = start_date_object,
            read_time__lte = end_date_object
        )


class ReadingList(generics.ListCreateAPIView):
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        start_date = self.request.query_params.get('start', None)
        start_date_object = datetime.datetime.today() - datetime.timedelta(days = 7) # Default to a week's worth
        if start_date != None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get('end', None)
        end_date_object = datetime.datetime.today()
        if end_date != None:
            end_date_object = dateutil.parser.parse(end_date)

        return Reading.objects.filter(
            read_time__gte = start_date_object,
            read_time__lte = end_date_object
        )

class ReadingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save()

    def get_queryset(self):
        start_date = self.request.query_params.get('start', None)
        start_date_object = datetime.datetime.today() - datetime.timedelta(days = 7) # Default to a week's worth
        if start_date != None:
            start_date_object = dateutil.parser.parse(start_date)

        end_date = self.request.query_params.get('end', None)
        end_date_object = datetime.datetime.today()
        if end_date != None:
            end_date_object = dateutil.parser.parse(end_date)

        queryset = Message.objects.filter(
            arrival_time__gte = start_date_object,
            arrival_time__lte = end_date_object
        )

        goes_id = self.request.query_params.get('goes_id', None)
        if goes_id is not None:
            queryset = Message.objects.filter(
                arrival_time__gte = start_date_object,
                arrival_time__lte = end_date_object,

                goes_id = goes_id
            )

        return queryset

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
