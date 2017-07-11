from django.conf.urls import url
from climate_exporter import views

urlpatterns = [
    url(r'^$', views.index),
]
