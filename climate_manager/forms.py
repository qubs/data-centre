from django import forms

from climate_data.models import *


class InvalidateDataForm(forms.Form):
    station = forms.ModelChoiceField(queryset=Station.objects.all())
    data_type = forms.ModelChoiceField(queryset=DataType.objects.all())

    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()


class DataTypeInvalidateDataForm(forms.Form):
    station = forms.ModelChoiceField(queryset=Station.objects.all())

    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()


class StationDataTypeInvalidateDataForm(forms.Form):
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()


class LogUploadForm(forms.Form):
    LOG_FORMAT_CHOICES = (
        ('satlink_std', 'Satlink Standard CSV (SatLink2)'),
        ('sutron_std', 'Sutron Standard CSV (XLite, SatLink3)'),
        ('pendant_event', 'HOBO Pendant Event Logger CSV'),
    )

    format = forms.ChoiceField(choices=LOG_FORMAT_CHOICES)
    log = forms.FileField()
