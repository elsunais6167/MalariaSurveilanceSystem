from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'category', 'address', 'supervisor', 'phone', 'email']


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'care_centre', 'address']


class DianosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['mode_of_diagnosis', 'dianosis_type', 'results', 'malaria_type', 'parasitemia_load', 'comment']