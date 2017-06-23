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


from django.conf.urls import url, include
from api import views


API_TITLE = 'QUBS Data API'
API_DESCRIPTION = 'A web API for accessing data provided by the Queen\'s University Biological Station'


urlpatterns = [
    url(r'^$', views.api_root, name='qubs-api-root'),

    url(r'^climate/', include('climate_data.urls')),
    url(r'^herbarium/', include('herbarium_data.urls')),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    url(r'^api-auth/', include('rest_framework.urls')),
]
