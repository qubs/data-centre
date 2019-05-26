import django_filters

from herbarium_data.models import *


CHAR_FIELD_LOOKUPS = ('exact', 'iexact', 'icontains', 'istartswith', 'iendswith', 'in')
TEXT_FIELD_LOOKUPS = ('exact', 'iexact', 'icontains', 'istartswith', 'iendswith')
INTEGER_FIELD_LOOKUPS = ('exact', 'lt', 'lte', 'gt', 'gte', 'in')
BOOLEAN_FIELD_LOOKUPS = ('exact',)


class SpecimenFilter(django_filters.FilterSet):
    class Meta:
        model = Specimen
        fields = {
            'id': INTEGER_FIELD_LOOKUPS,

            'dataset': CHAR_FIELD_LOOKUPS,

            'genus': CHAR_FIELD_LOOKUPS,
            'species': CHAR_FIELD_LOOKUPS,
            'common_name': CHAR_FIELD_LOOKUPS,

            'dth': CHAR_FIELD_LOOKUPS,
            'accession': CHAR_FIELD_LOOKUPS,

            'year_collected': INTEGER_FIELD_LOOKUPS,
            'month_collected': INTEGER_FIELD_LOOKUPS,
            'day_collected': INTEGER_FIELD_LOOKUPS,

            'map_included': BOOLEAN_FIELD_LOOKUPS,

            'collectors': TEXT_FIELD_LOOKUPS,

            'location': CHAR_FIELD_LOOKUPS,
            'habitat': CHAR_FIELD_LOOKUPS,

            'notes': TEXT_FIELD_LOOKUPS
        }
