from django.conf.urls import url, include
from django.contrib import admin


admin.site.site_header = 'QUBS Data Centre Admin'

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
]
