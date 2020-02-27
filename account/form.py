from django.forms import ModelForm
from .models import  profile
from django import forms

class profile_update_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = [ 'image', 'address','document10','document12','document_last_sem']

        labels = {

            'image': 'Profile pic',
            'address': 'Address',
            'document10': 'class 10th marksheet(.jpg)',
            'document12': 'class 12th marksheet(.jpg)',
            'document_last_sem': 'Last year marsheet(.jpg)'
        }


