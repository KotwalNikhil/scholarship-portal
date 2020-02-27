from django.forms import ModelForm
from .models import  scholarship
from django import forms


class add_scholarship_form(forms.ModelForm):
    class Meta:
        model = scholarship
        fields = ['title', 'applicants', 'short_description','long_description','img','boy','girl','both','active','document','fromdate','toomdate']

        # labels = {
        #     'email': 'Email',
        #     'image': 'Profile pic',
        #     'address': 'Address',
        #     'document10': 'class 10th marksheet(.jpg)',
        #     'document12': 'class 12th marksheet(.jpg)',
        #     'document_last_sem': 'Last year marsheet(.jpg)'
        # }
