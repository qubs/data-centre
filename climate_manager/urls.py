from django.conf.urls import url
from climate_manager import views

urlpatterns = [
    url(r'^$', views.index, name='climate-manager-index'),

    url(r'^stations/(?P<pk>[0-9]+)/$', views.station_overview, name='station'),
    url(r'^stations/(?P<pk>[0-9]+)/(?P<data_type>[a-zA-Z0-9_]+)/$', views.station__data_type,
        name='station__data_type'),
    url(r'^stations/(?P<pk>[0-9]+)/(?P<data_type>[a-zA-Z0-9_]+)/chart.png$',
        views.station_chart, name='station__data_type__chart'),

    url(r'^data-types/(?P<data_type>[a-zA-Z0-9_]+)/$', views.data_type_overview,
        name='data_type')
]
