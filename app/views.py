from django.shortcuts import render, redirect, get_object_or_404

#models
from .models import Patient
from .models import Station
from .models import Morbidity
from .models import Mortality
from .models import Preventive
from .models import Household
from .models import Diagnosis
from .models import Treatment

#forms
from .forms import HouseholdForm
from .forms import PreventionForm
from .forms import TreatmentForm
from .forms import PatientForm
from .forms import StationForm
from .forms import DianosisForm
from .forms import MorbidityForm
from .forms import MortalityForm

# Create your views here.
def index(request):

    context = {

    }

    return render(request, 'index.html', context)

def household(request):
    form = HouseholdForm()
    if request.method == "POST":
        form = HouseholdForm(request.POST)
        if form.is_valid():
            #user = request.user
            # Create a new product and set the user field
            house = form.save(commit=False)
            #customer.user = user
            house.save()
            return redirect('household')

    context = {
        'form': form, 
    }
    return render(request, 'household.html', context)

def addStation(request):
    form = StationForm()
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            #user = request.user
            
            station = form.save(commit=False)
            #station.user = user
            station.save()
            return redirect('addStation')

    context = {
        'form': form, 
    }

    return render(request, 'station.html', context)

def addPatient(request):
    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            #user = request.user
            patient = form.save(commit=False)
            #customer.user = user
            patient.save()
            return redirect('home')

    context = {
        'form': form, 
    }

    return render(request, 'patient.html', context)

def addDiagnosis(request):
    form = DianosisForm()
    if request.method == 'POST':
        form = DianosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.save()
            return redirect('home')
    context = {
        'form':form
    }

    return render(request, 'diagnosis.html', context)

def addMorbidity(request):
    form = MorbidityForm()
    if request.method == 'POST':
        form = MorbidityForm(request.POST)
        if form.is_valid():
            morbidity = form.save(commit=False)
            morbidity.save()
            return redirect('home')
        
    context = {
        'form':form
    }

    return render(request, 'morbidity.html', context)

def addMortality(request):
    form = MortalityForm()
    if request.method == 'POST':
        form = MortalityForm(request.POST)
        if form.is_valid():
            mortality = form.save(commit=False)
            mortality.save()
            return redirect('home')
        
    context = {
        'form':form
    }

    return render(request, 'mortality.html', context)

def addTreatment(request):
    form = TreatmentForm()
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.save()
            return redirect('home')
        
    context = {
        'form': form
    }

    return render(request, 'treatment.html', context)

def addPreventive(request):
    form = PreventionForm()
    if request.method == 'POST':
        form = PreventionForm(request.POST)
        if form.is_valid():
            prevention = form.save(commit=False)
            prevention.save()
            return redirect('home')
        
    context = {
        'form': form
    }

    return render(request, 'prevention.html', context)

def adminDash(request):
    station_list = Station.objects.all()
    

    context = {
        'station_list': station_list,
        
    }

    return render(request, 'admin_dash.html', context)

def stationDash(request, pk):
    station_id = get_object_or_404(Station, id=pk)
    context = {

    }
    return render(request, 'station_dash.html', context)