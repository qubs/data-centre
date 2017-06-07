from django.contrib import admin
from api_herbarium.models import *


@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    pass
