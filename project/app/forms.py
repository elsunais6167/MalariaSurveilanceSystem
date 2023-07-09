from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=70)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'category', 'address',
                  'supervisor', 'phone', 'email', 'gis_location']
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
        fields = ['name', 'gender', 'age', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DianosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['mode_of_diagnosis', 'dianosis_type', 'results',
                  'malaria_type', 'parasitemia_load', 'comment']
        widgets = {
            'parasitemia_load': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_of_diagnosis': forms.Select(attrs={'class': 'form-control'}),
            'dianosis_type': forms.Select(attrs={'class': 'form-control'}),
            'results': forms.Select(attrs={'class': 'form-control'}),
            'malaria_type': forms.Select(attrs={'class': 'form-control'}),
            'parasitemia_load': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'dianosis_type': 'Type of Diagnosis'
        }


class HouseholdForm(ModelForm):
    class Meta:
        model = Household
        fields = ['family_size', 'no_of_children',
                  'sleeping_in_screen', 'drainage_system']
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


class MorbidityForm(ModelForm):
    class Meta:
        model = Morbidity
        fields = ['severity', 'mode_of_admission', 'comment']
        widgets = {
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'mode_of_admission': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class MortalityForm(ModelForm):
    class Meta:
        model = Mortality
        fields = ['status', 'date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control'}),
                
        }

class TreatmentForm(ModelForm):
    class Meta:
        model = Treatment
        fields = ['treatment_type', 'treatment_period', 'follow_up',  'further_treatment', 'comment']
        widgets = {
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'treatment_period': forms.Select(attrs={'class': 'form-control'}),
            'follow_up': forms.Select(attrs={'class': 'form-control'}),
            'further_treatment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'follow_up': 'Select, IF there is Follow-Up Diagnosis'
        }

class PreventionForm(ModelForm):
    class Meta:
        model = Preventive
        fields = ['use_of_mosquito_net', 'use_of_insecticide', 'use_of_repellant',  'indoor_residual']
        widgets = {
            'indoor_residual': forms.Select(attrs={'class': 'form-control'}),
            'use_of_mosquito_net': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'use_of_insecticide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'use_of_repellant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number'
        }

class MakeAdmin(ModelForm):
    class Meta:
        model = Station_admin
        fields = ['user']
        widgets = {
            'user' : forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'user': 'Select User to Assign as a Station Admin'
        }