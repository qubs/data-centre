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


from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'^$', views.api_root),

    url(r'^sensors/$', views.SensorList.as_view(), name='sensor-list'),
    url(r'^sensors/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor-detail'),
    url(r'^sensors/(?P<pk>[0-9]+)/data/$', views.SensorData.as_view(), name='sensor-data'),
    url(r'^sensors/(?P<pk>[0-9]+)/stations/$', views.SensorStations.as_view(), name='sensor-stations'),


    url(r'^stations/$', views.StationList.as_view(), name='station-list'),
    url(r'^stations/(?P<pk>[0-9]+)/$', views.StationDetail.as_view(), name='station-detail'),
    url(r'^stations/(?P<pk>[0-9]+)/data/$', views.StationData.as_view(), name='station-data'),
    url(r'^stations/(?P<pk>[0-9]+)/sensors/$', views.StationSensors.as_view(), name='station-sensors'),
    url(r'^stations/(?P<pk>[0-9]+)/messages/$', views.StationMessages.as_view(), name='station-messages'),

    url(r'^station-sensor-links/$', views.StationSensorLinkList.as_view(), name='station-sensor-link-list'),
    url(r'^station-sensor-links/(?P<pk>[0-9]+)/$', views.StationSensorLinkDetail.as_view(), name='station-sensor-link-detail'),

    url(r'^readings/$', views.ReadingList.as_view(), name='reading-list'),
    url(r'^readings/(?P<pk>[0-9]+)/$', views.ReadingDetail.as_view(), name='reading-detail'),

    url(r'^messages/$', views.MessageList.as_view(), name='message-list'),
    url(r'^messages/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view(), name='message-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]
