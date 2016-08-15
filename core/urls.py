from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^$', views.api_root),

    url(r'^sensors/$', views.SensorList.as_view(), name='sensor-list'),
    url(r'^sensors/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor-detail'),
    url(r'^sensors/(?P<pk>[0-9]+)/data/$', views.SensorData.as_view(), name='sensor-data'),

    url(r'^stations/$', views.StationList.as_view(), name='station-list'),
    url(r'^stations/(?P<pk>[0-9]+)/$', views.StationDetail.as_view(), name='station-detail'),

    url(r'^readings/$', views.ReadingList.as_view(), name='reading-list'),
    url(r'^readings/(?P<pk>[0-9]+)/$', views.ReadingDetail.as_view(), name='reading-detail'),

    url(r'^messages/$', views.MessageList.as_view(), name='message-list'),
    url(r'^messages/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view(), name='message-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]
