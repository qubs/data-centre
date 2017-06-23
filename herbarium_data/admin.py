from django.contrib import admin
from herbarium_data.models import *


@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ["accession", "dataset", "latin_name", "common_name", "date_collected_str"]
    list_filter = ["dataset", "map_included"]
    ordering = ["genus", "species"]
    pass
