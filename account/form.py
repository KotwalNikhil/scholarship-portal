from django.forms import ModelForm
from .models import  profile
from django import forms
from django.contrib.auth.models import User


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
        fields = [ 'address','roll_no','marks','present_year','image','attendence','mobile','document10','document12','document_last_sem','father_id','father_name' ,'father_rank','student_id']

        widgets = {
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'roll_no':forms.NumberInput(attrs={'readonly':False,'class':'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'present_year': forms.Select(attrs={'class': 'form-control'}),
            'father_rank':forms.Select(attrs={'class':'form-control'}),
            'attendence': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),

        }

class Profile_Form_for_admin_work(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'email':forms.TextInput(attrs={'readonly': False}),
            'first_name':forms.TextInput(attrs={'readonly': True}),
        }
    def __init__(self, *args, **kwargs):
        super(Profile_Form_for_admin_work, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class Profile2_form_for_admin_work(forms.ModelForm):
    class Meta:
        model = profile
        fields = [ 'address','roll_no','marks','present_year','image','attendence','document10','document12','document_last_sem','father_id','father_name' ,'father_rank','student_id']

        widgets = {
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'roll_no':forms.NumberInput(attrs={'class':'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'present_year': forms.Select(attrs={'class': 'form-control'}),
            'father_rank':forms.Select(attrs={'class':'form-control'}),
            'attendence': forms.NumberInput(attrs={ 'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={ 'class': 'form-control'}),

        }
