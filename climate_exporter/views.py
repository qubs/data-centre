import csv
from lxml import etree
from datetime import datetime

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from climate_exporter.forms import ExportForm

from climate_data.models import *
from climate_data.serializers import *


class PseudoBuffer(object):
    def write(self, value):
        return value


def index(request):
    station_data_types = {}
    for s in Station.objects.all().iterator():
        station_data_types[s.id] = list(map(
            lambda l: l.data_type.id,
            StationSensorLink.objects.filter(station=s).iterator()
        ))

    if request.method == 'POST':
        form = ExportForm(request.POST)

        if form.is_valid():
            include_invalid = form.cleaned_data['include_invalid']
            include_out_of_bounds = form.cleaned_data['include_out_of_bounds']
            only_use_qc = form.cleaned_data['only_use_qc']

            time_start = form.cleaned_data['time_start']
            time_end = form.cleaned_data['time_end']

            format = form.cleaned_data['format']

            station = form.cleaned_data['station']
            data_types = form.cleaned_data['data_types']

            links = StationSensorLink.objects.filter(station=station).select_related('data_type')

            queryset = Reading.objects.filter(station=station).order_by('-read_time')

            if not include_invalid:
                queryset = queryset.filter(invalid=False)

            if only_use_qc:
                queryset = queryset.filter(qc_processed=True)

            if time_start:
                queryset = queryset.filter(read_time__gte=time_start)

            if time_end:
                queryset = queryset.filter(read_time__lte=time_end)

            if len(data_types) > 0:
                queryset = queryset.filter(station_sensor_link__data_type__in=data_types)\
                    .select_related('sensor', 'station_sensor_link', 'station_sensor_link__data_type')

            if format == 'csv':
                header = ['time']

                for link in links:
                    if link.data_type in data_types:
                        header.append(link.data_type.short_name)

                rows = [header]

                # Since rows are ordered by time, we can sort of piecemeal build up non-long form rows of data.

                current_row_time = None
                current_row = []

                for reading in queryset:
                    if current_row_time is None:
                        current_row_time = reading.read_time

                    if current_row_time != reading.read_time:
                        # Time to send the current row to the CSV, since we've moved past that particular read time.

                        ordered_row = [current_row_time]

                        for measurement in header:
                            if measurement != 'time':  # Ignore this, since it has a fixed position and is always there.
                                for label, value, in_bounds in current_row:
                                    if label == measurement:
                                        if include_out_of_bounds or in_bounds:
                                            ordered_row.append(value)

                        rows.append(ordered_row)

                        current_row_time = reading.read_time
                        current_row = []

                    current_row.append((reading.data_type().short_name, reading.decimal_value_str(),
                                        reading.in_bounds()))

                # Send a streaming response back to prevent any timing out issues.

                pseudo_buffer = PseudoBuffer()
                writer = csv.writer(pseudo_buffer)

                response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'

                return response

            elif format == 'json':
                pass

            elif format == 'xml':
                root = etree.Element('report', station=station.name, generation_time=datetime.now().isoformat())

                current_reading_set_time = None
                current_reading_set = etree.Element('reading_set')

                for reading in queryset:
                    if current_reading_set_time is None:
                        current_reading_set_time = reading.read_time

                    if current_reading_set_time != reading.read_time:
                        # Time to send the current reading set to the XML, since we've moved past that particular
                        # read time.

                        current_reading_set.set('time', current_reading_set_time.isoformat())
                        root.append(current_reading_set)

                        current_reading_set_time = reading.read_time
                        current_reading_set = etree.Element('reading_set')

                    reading_element = etree.Element(reading.data_type().short_name)
                    reading_element.text = reading.decimal_value_str()

                    current_reading_set.append(reading_element)

                response = HttpResponse(etree.tostring(root), content_type='text/xml')
                response['Content-Disposition'] = 'attachment; filename="report.xml"'

                return response

            return HttpResponseBadRequest()  # No valid format specified...

    else:  # GET request
        form = ExportForm()

    return render(request, 'climate_exporter/index.html', {
        'form': form,
        'station_data_types': JSONRenderer().render(station_data_types)
    })
