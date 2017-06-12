from django.contrib import admin
from herbarium_data.models import *


@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    pass
