import django_filters


class SpecimenFilter(django_filters.FilterSet):
    class Meta:
        model = Specimen
        fields = {
            'genus': ('exact', 'iexact', 'icontains'),
            'species': ('exact', 'iexact', 'icontains'),
            'common_name': ('exact', 'iexact', 'icontains'),

            'dth': ('exact', 'iexact', 'icontains'),
            'accession': ('exact', 'iexact', 'icontains'),

            'year_collected': ('exact', 'lt', 'lte', 'gt', 'gte'),
            'month_collected': ('exact', 'lt', 'lte', 'gt', 'gte'),
            'day_collected': ('exact', 'lt', 'lte', 'gt', 'gte')
        }
