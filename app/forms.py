from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=70)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'category', 'address', 'supervisor', 'phone', 'email', 'gis_location']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gis_location': forms.HiddenInput(),
        }

        labels = {
            'name': 'Name of Collection Centre/Program',
            'category': 'What type of Collection Centre',
        }
        
        

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'care_centre', 'address']


class DianosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['mode_of_diagnosis', 'dianosis_type', 'results', 'malaria_type', 'parasitemia_load', 'comment']

class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = ['family_size', 'no_of_children', 'sleeping_in_screen', 'drainage_system']
        widgets = {
            'family_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_of_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'sleeping_in_screen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'drainage_system': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'family_size': 'Family Size',
            'no_of_children': 'Number of Children',
            'sleeping_in_screen': 'Sleeping in Screen House',
            'drainage_system': 'Type of Drainage System',
        }