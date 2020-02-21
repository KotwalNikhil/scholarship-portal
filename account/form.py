from django.forms import ModelForm
from .models import  profile
from django import forms

class profile_update_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['email', 'image', 'address','document10','document12','document_last_sem']




