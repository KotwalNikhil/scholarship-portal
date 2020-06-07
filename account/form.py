from django.forms import ModelForm
from .models import  profile
from django import forms
from django.contrib.auth.models import User

# class profile_update_form(forms.ModelForm):
#     class Meta:
#         model = profile
#         fields = [ 'image', 'address','document10','document12','document_last_sem','father_id' ,'student_id','father_name']
#
#         labels = {
#
#             'image': 'Profile pic',
#             'address': 'Address',
#             'document10': 'class 10th marksheet(.jpg)',
#             'document12': 'class 12th marksheet(.jpg)',
#             'document_last_sem': 'Last year marsheet(.jpg)',
#             'father_id':'Father Identity card',
#             'father_name': 'Father Name',
#
#             'student_id':'Student Identity/dependent card '
#         }

class Profile_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'email':forms.TextInput(attrs={'readonly': True}),
            'first_name':forms.TextInput(attrs={'readonly': True}),
        }
    def __init__(self, *args, **kwargs):
        super(Profile_Form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class Profile2_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = [ 'address','roll_no','marks','branch','image','attendence','document10','document12','document_last_sem','father_id','father_name' ,'father_rank','student_id']

        widgets = {
            'branch':forms.NumberInput(attrs={'readonly':True,'class':'form-control form-control-alternative'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'roll_no':forms.NumberInput(attrs={'readonly':True,'class':'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_rank':forms.Select(attrs={'class':'form-control'}),
            'attendence': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),

        }

