import json
import datetime
import pytz
import numpy

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.dates import DateFormatter, date2num

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from climate_manager.forms import *

from climate_data.models import *
from climate_data.serializers import *


@login_required
def index(request):
    station_data_types = {
        s.id: [l.data_type.id for l in StationSensorLink.objects.filter(station=s).iterator()]
        for s in Station.objects.all().iterator()
    }

    if request.method == 'POST':
        form = InvalidateDataForm(request.POST)

        if form.is_valid():
            station = form.cleaned_data['station']
            data_type = form.cleaned_data['data_type']

            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']

            queryset = Reading.objects.filter(
                station=station,
                station_sensor_link__data_type=data_type,

                read_time__gte=time_start,
                read_time__lte=time_end,

                invalid=False  # Don't bother re-invalidating readings - plus, it throws the count off.
            )

            count = queryset.count()

            if count > 0:
                queryset.update(invalid=True, qc_processed=True)

                messages.success(
                    request,
                    'Invalidated {count} readings from {station_name} on interval [{s}, {e}].'.format(
                        count=count,
                        station_name=station.name,

                        s=time_start,
                        e=time_end
                    )
                )
            else:
                messages.info(request, 'No (non-invalid) readings were found within those restrictions.')

        else:
            messages.error(request, 'The command submitted was not valid.')

    else:
        form = InvalidateDataForm()

    return render(request, 'climate_manager/index.html', {
        'invalidation_form': form,

        'stations': list(Station.objects.all().values()),
        'stations_json': JSONRenderer().render([StationSerializer(s).data for s in Station.objects.all().iterator()])
                                       .decode('utf-8'),
        'station_data_types': JSONRenderer().render(station_data_types).decode('utf-8')
    })


@login_required
def station_overview(request, pk=None):
    try:
        pk = int(pk)
    except TypeError:
        return HttpResponseBadRequest()

    try:
        station = Station.objects.get(id=pk)
    except Station.DoesNotExist:
        raise Http404('Station does not exist')

    if request.method == 'POST':
        log_upload_form = LogUploadForm(request.POST)

        # if log_upload_form.is_valid():

    else:
        log_upload_form = LogUploadForm()

    station_data_types = [
        l.data_type for l in StationSensorLink.objects.filter(station=station).select_related('data_type').iterator()
    ]

    return render(request, 'climate_manager/station.html', {
        'station': station,
        'log_upload_form': log_upload_form,
        'station_data_types': [DataTypeSerializer(d).data for d in station_data_types],
    })


@login_required
def station__data_type(request, pk=None, data_type=None):
    try:
        pk = int(pk)
    except TypeError:
        return HttpResponseBadRequest()

    if data_type is None:
        return HttpResponseBadRequest()

    try:
        station = Station.objects.get(id=pk)
    except Station.DoesNotExist:
        raise Http404('Station does not exist')

    try:
        data_type = DataType.objects.get(short_name=data_type)
    except DataType.DoesNotExist:
        raise Http404('Data type does not exist')

    station_sensor_link = StationSensorLink.objects.get(station=station, data_type=data_type)

    if request.method == 'POST':
        form = StationDataTypeInvalidateDataForm(request.POST)

        if form.is_valid():
            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']

            queryset = Reading.objects.filter(
                station=station,
                station_sensor_link__data_type=data_type,

                read_time__gte=time_start,
                read_time__lte=time_end,

                invalid=False  # Don't bother re-invalidating readings - plus, it throws the count off.
            )

            count = queryset.count()

            if count > 0:
                queryset.update(invalid=True, qc_processed=True)

                messages.success(
                    request,
                    'Invalidated {count} readings on interval [{s}, {e}].'.format(
                        count=count,
                        station_name=station.name,

                        s=time_start,
                        e=time_end
                    )
                )
            else:
                messages.info(request, 'No (non-invalid) readings were found within those restrictions.')

        else:
            messages.error(request, 'The command submitted was not valid.')

    else:
        form = StationDataTypeInvalidateDataForm()

    # Fetch data after potential invalidations.
    graph_data = [[r.read_time, r.decimal_value()] for r in Reading.objects.filter(
        station_sensor_link=station_sensor_link,
        invalid=False
    ).only('read_time', 'value', 'sensor').select_related('sensor').order_by('read_time').iterator()]

    return render(request, 'climate_manager/station__data_type.html', {
        'invalidation_form': form,

        'station': station,
        'data_type': data_type,
        'graph_data': JSONRenderer().render(graph_data).decode('utf-8')
    })


def station_chart(request, pk=None, data_type=None):
    try:
        pk = int(pk)
    except TypeError:
        return HttpResponseBadRequest()

    if data_type is None:
        return HttpResponseBadRequest()

    try:
        station = Station.objects.get(id=pk)
    except Station.DoesNotExist:
        raise Http404('Station does not exist')

    try:
        data_type = DataType.objects.get(short_name=data_type)
    except DataType.DoesNotExist:
        raise Http404('Data type does not exist')

    station_sensor_link = StationSensorLink.objects.get(station=station, data_type=data_type)

    data = list(Reading.objects.filter(
        station_sensor_link=station_sensor_link,
        invalid=False,
        read_time__gte=datetime.datetime.now(pytz.utc)-datetime.timedelta(days=31)
    ).only('read_time', 'value', 'sensor').select_related('sensor').order_by('read_time'))

    chart = Figure()
    ax = chart.add_subplot(111)

    x = [r.read_time for r in data if (r.decimal_value() is None or r.decimal_value() in data_type.bounds)]
    y = [r.decimal_value() for r in data if (r.decimal_value() is None or r.decimal_value() in data_type.bounds)]

    all_nan = True

    for i in range(0, len(y)):
        if y[i] is None:
            y[i] = numpy.nan
        elif all_nan:
            all_nan = False

    if all_nan:
        # Prevent a strange error with date axis conversion from matplotlib.
        x = []
        y = []

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    chart.autofmt_xdate()

    response = HttpResponse(content_type='image/png')
    FigureCanvasAgg(chart).print_png(response)

    return response


@login_required
def data_type_overview(request, data_type=None):
    if data_type is None:
        return HttpResponseBadRequest()

    try:
        data_type = DataType.objects.get(short_name=data_type)
    except DataType.DoesNotExist:
        raise Http404('Data type does not exist')

    if request.method == 'POST':
        form = DataTypeInvalidateDataForm(request.POST)

        if form.is_valid():
            station = form.cleaned_data['station']

            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']

            queryset = Reading.objects.filter(
                station=station,
                station_sensor_link__data_type=data_type,

                read_time__gte=time_start,
                read_time__lte=time_end,

                invalid=False  # Don't bother re-invalidating readings - plus, it throws the count off.
            )

            count = queryset.count()

            if count > 0:
                queryset.update(invalid=True, qc_processed=True)

                messages.success(
                    request,
                    'Invalidated {count} readings from {station_name} on interval [{s}, {e}].'.format(
                        count=count,
                        station_name=station.name,

                        s=time_start,
                        e=time_end
                    )
                )
            else:
                messages.info(request, 'No (non-invalid) readings were found within those restrictions.')

        else:
            messages.error(request, 'The command submitted was not valid.')

    else:
        form = DataTypeInvalidateDataForm()

    # Fetch data after potential invalidations.
    graph_data = [{
        'name': s.name,
        'data': [[r.read_time, r.decimal_value()] for r in Reading.objects.filter(
            station_sensor_link__station=s,
            station_sensor_link__data_type=data_type,
            invalid=False
        ).only('read_time', 'value', 'sensor', 'station_sensor_link').select_related('sensor', 'station_sensor_link')
            .order_by('read_time').iterator()]
    } for s in Station.objects.all().iterator()]

    return render(request, 'climate_manager/data_type.html', {
        'invalidation_form': form,

        'data_type': data_type,
        'graph_data': JSONRenderer().render(graph_data).decode('utf-8')
    })
