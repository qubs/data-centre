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


from django.contrib import admin
from climate_data.models import *


def invalidate_reading(modeladmin, request, queryset):
    queryset.update(invalid=True)

invalidate_reading.short_description = "Mark selected readings as 'invalid'"


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "unit")
    ordering = ["name"]


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "decimals")


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "goes_id")


@admin.register(StationSensorLink)
class StationSensorLinkAdmin(admin.ModelAdmin):
    list_display = ("station", "sensor", "data_type", "read_frequency", "station_order")
    list_editable = ("sensor", "data_type")
    list_filter = ("data_type",)
    ordering = ["station", "station_order"]


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ("read_time", "station", "sensor", "decimal_value_str", "data_source", "qc_processed", "invalid")
    list_filter = ("station", "qc_processed")
    ordering = ["-read_time", "station", "sensor"]
    actions = [invalidate_reading]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("arrival_time", "station", "goes_id", "data_quality", "data_source", "recorded_message_length")
    list_filter = ("goes_id", "data_quality")
    ordering = ["-arrival_time"]
    pass
