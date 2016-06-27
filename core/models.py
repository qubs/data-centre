# Copyright 2016 Queen's University Biological Station

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models


class Sensor(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=100)
	data_id = models.CharField(max_length=20) # For downloaded data, sometimes the full name would be unwieldy

	decimals = models.PositiveSmallIntegerField()

class Station(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=100)
	goes_id = models.CharField(max_length=8)

	sensors = models.ManyToManyField(Sensor)

class Reading(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	read_time = models.DateTimeField()
	value = models.IntegerField()

	sensor = models.ForeignKey("Sensor", on_delete=models.SET_NULL, null=True)
	station = models.ForeignKey("Station", on_delete=models.SET_NULL, null=True)

