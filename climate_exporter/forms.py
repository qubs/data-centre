from django import forms

from climate_data.models import *


class ExportForm(forms.Form):
    FORMATS = (
        ('csv', 'Comma-Separated Values (CSV)'),
        ('json', 'JSON'),
        ('xml', 'XML'),
    )

    include_invalid = forms.BooleanField(label='Include Invalid Readings', required=False)
    include_out_of_bounds = forms.BooleanField(label='Include Out-of-Bounds Readings', required=False)
    only_use_qc = forms.BooleanField(label='Only Include Quality-Controlled Readings', required=False)

    time_start = forms.DateTimeField(label='Data Start Time', required=False)
    time_end = forms.DateTimeField(label='Data End Time', required=False)

    station = forms.ModelChoiceField(queryset=Station.objects.all())
    data_types = forms.ModelMultipleChoiceField(queryset=DataType.objects.all(), widget=forms.CheckboxSelectMultiple)

    format = forms.ChoiceField(choices=FORMATS)
