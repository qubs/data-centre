from django.contrib import admin
from herbarium.models import *


@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    pass
