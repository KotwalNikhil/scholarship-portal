

from django.forms import ModelForm
from .models import  scholarship
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class add_scholarship_form(forms.ModelForm):



    class Meta:
        model = scholarship
        fields = ['title', 'applicants', 'short_description','long_description','img','boy','girl','both','active','document','fromdate','toomdate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'special'}),
            'fromdate': DateInput(),
            'toomdate': DateInput(),
        }

        labels = {
            'title': 'Title',
            'applicants': 'Applicants',
            'short_description': 'Short_description',
            'img': 'Picture',
            'both': ' For both(boys and girls)',
            'fromdate': 'Starting date',
            'toomdate': 'End date',
        }