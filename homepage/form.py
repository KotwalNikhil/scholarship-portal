

from django.forms import ModelForm
from .models import  scholarship,application_table
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class add_scholarship_form(forms.ModelForm):
    class Meta:
        model = scholarship
        fields = ['title','short_description','long_description','img','both','boy','girl','active','document','scholarship_form','fromdate','toomdate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'special'}),
            'fromdate': DateInput(),
            'toomdate': DateInput(),
        }

        labels = {
            'title': 'Title',
            'short_description': 'Short_description',
            'img': 'Picture',
            'both': ' Total(boys and girls)per branch',
            'boy':'Boys per branch( if distributed in boys and girls else leave -1)',
            'girl':'Girls per branch( if distributed in boys and girls else leave -1)',
            'document':'Scholarship SOP',
            'fromdate': 'Starting date (Make sure it is less then or equal to today"s date)',
            'toomdate': 'End date',
        }

class extra_documents_form(forms.ModelForm):
    class Meta:
        model = application_table
        fields = ['applied_extra1','applied_extra2', 'applied_scholarship_form']
        labels = {
            'applied_scholarship_form':'Application form(Only in pdf)',
            'applied_extra1': 'Other Document 1',
            'applied_extra2': 'Other Document 2',

        }