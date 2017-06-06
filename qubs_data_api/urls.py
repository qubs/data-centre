from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^climate/', include('climate.urls')),
    url(r'^herbarium/', include('herbarium.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
]
