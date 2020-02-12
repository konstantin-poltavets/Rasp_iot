from django import forms
import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from .models import gaz, CalcManager, Calc


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


class MyForm(forms.Form):
    date_field = forms.DateField(widget=DatePicker())
    date_field_required_with_min_max_date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '2009-01-20',
                'maxDate': '2017-01-20',
            },
        ),
    )
    time_field = forms.TimeField(
        widget=TimePicker(
            options={
               # 'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
            },
            attrs={
                'input_toggle': True,
                'input_group': True,
            },
        ),
    )
    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (
                    datetime.date.today() + datetime.timedelta(days=1)
                ).strftime(
                    '%Y-%m-%d'
                ),  # Tomorrow
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )


class gazForm(forms.ModelForm):
    class Meta:
        model = gaz
        fields = ['created_date', 'millage', 'station_type','id', 'fuel_type', 'liters', 'price']


class CalcForm(forms.ModelForm):
    class Meta:
        model = Calc

        fields = ['first', 'second']