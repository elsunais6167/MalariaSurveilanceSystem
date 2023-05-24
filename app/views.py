from django.shortcuts import render, redirect

#models
from .models import Patient
from .models import Station

#forms
from .forms import HouseholdForm
from .forms import PatientForm
from .forms import StationForm

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
            # Create a new product and set the user field
            station = form.save(commit=False)
            #customer.user = user
            station.save()
            return redirect('addStation')

    context = {
        'form': form, 
    }

    return render(request, 'station.html', context)