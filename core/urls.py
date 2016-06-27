from django.conf.urls import url
from core import views

urlpatterns = [
	url(r'^sensors/$', views.SensorList.as_view()),
	url(r'^sensors/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view()),

	url(r'^stations/$', views.StationList.as_view()),
	url(r'^stations/(?P<pk>[0-9]+)/$', views.StationDetail.as_view()),

	url(r'^readings/$', views.ReadingList.as_view()),
	url(r'^readings/(?P<pk>[0-9]+)/$', views.ReadingDetail.as_view()),
]
