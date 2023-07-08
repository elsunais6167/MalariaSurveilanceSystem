from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

#models
from .models import Patient
from .models import Station
from .models import Morbidity
from .models import Mortality
from .models import Preventive
from .models import Household
from .models import Diagnosis
from .models import Treatment
from .models import User_admin
from .models import Station_admin

#forms
from .forms import CreateUserForm
from .forms import HouseholdForm
from .forms import PreventionForm
from .forms import TreatmentForm
from .forms import PatientForm
from .forms import StationForm
from .forms import DianosisForm
from .forms import MorbidityForm
from .forms import MortalityForm

# Create your views here.
def is_user_admin(user):
    return hasattr(user, 'user_admin')

def is_station_admin(user):
    return hasattr(user, 'station_admin')

def index(request):
    error_message = ""
    login_error = ""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'station_admin'):
                return redirect('sta-admin')
            elif hasattr(user, 'user_admin'):
                return redirect('admin-dash')
            else:
                error_message = 'Your login details are correct. However, you have not been assigned a Mosque to Manage. Please contact state coordinator'
        else:
            login_error ='Invalid Username or Password, Please Try Again!'
            
    return render(request, 'index.html', {'error_message': error_message, 'login_error': login_error})


def loggingout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
@user_passes_test(is_user_admin)
def user_signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_signup')
    else:
        form = CreateUserForm()
    
    
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


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

@login_required
@user_passes_test(is_user_admin)
def addStation(request):
    form = StationForm()
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            user = request.user
            station = form.save(commit=False)
            station.user = user
            station.save()
            return redirect('admin-dash')

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

@login_required
@user_passes_test(is_user_admin)
def adminDash(request):
    station_list = Station.objects.all()
    

    context = {
        'station_list': station_list,
        
    }

    return render(request, 'admin_dash.html', context)

def stationDash(request, pk):
    station_id = get_object_or_404(Station, id=pk)
    #station = Station.objects.all()
    context = {
        'station': station_id

    }
    return render(request, 'station_dash.html', context)

@login_required
def user_list(request):
    users_list = User.objects.all()
    context = {
        'users_list': users_list,
    }

    return render(request, 'users.html', context)

@login_required
@user_passes_test(is_user_admin)
def make_admin(request, pk):
    user_id = get_object_or_404(User, id=pk)

    context = {

    }
    return render(request, 'make_admin.html', context)

def station_admin(request):

    context = {

    }

    return render(request, 'station_admin.html', context)