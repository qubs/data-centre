from rest_framework import serializers

from herbarium_data.models import *


class SpecimenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specimen
        fields = ("id", "created", "updated",  "dataset", "genus", "species", "common_name", "dth", "accession",
                  "date_collected", "collectors", "map_included", "map_reference", "county", "township", "location",
                  "habitat", "notes", "image",)
