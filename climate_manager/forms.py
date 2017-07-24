from django import forms

from climate_data.models import *


class InvalidateDataForm(forms.Form):
    station = forms.ModelChoiceField(queryset=Station.objects.all())
    data_type = forms.ModelChoiceField(queryset=DataType.objects.all())

    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
