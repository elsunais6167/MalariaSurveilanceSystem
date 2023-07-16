from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

# models
from .models import CampReport, Campaign, Patient
from .models import Station
from .models import Morbidity
from .models import Mortality
from .models import Preventive
from .models import Household
from .models import Diagnosis
from .models import Treatment
from .models import User_admin
from .models import Station_admin
from .models import Profile

# forms
from .forms import CampaignForm, CreateUserForm
from .forms import HouseholdForm
from .forms import PreventionForm
from .forms import TreatmentForm
from .forms import PatientForm
from .forms import StationForm
from .forms import DianosisForm
from .forms import MorbidityForm
from .forms import MortalityForm
from .forms import ProfileForm
from .forms import MakeAdmin

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
            login_error = 'Invalid Username or Password, Please Try Again!'

    return render(request, 'index.html', {'error_message': error_message, 'login_error': login_error})

   
def loggingout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def login_user(request):
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
            login_error = 'Invalid Username or Password, Please Try Again!'

    return render(request, 'index.html', {'error_message': error_message, 'login_error': login_error})


@login_required
@user_passes_test(is_user_admin)
def user_signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dash')
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
            # user = request.user
            # Create a new product and set the user field
            house = form.save(commit=False)
            # customer.user = user
            house.save()
            return redirect('household')

    context = {
        'form': form,
    }
    return render(request, 'household.html', context)


def profile(request, id):
    p_id = get_object_or_404(User, id=id)
    p_id = p_id.id
    user_id = User.objects.get(id=p_id)
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = user_id
            # Create a new product and set the user field
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect('user-list')

    context = {
        'form': form,
        'p_id': p_id
    }
    return render(request, 'profile.html', context)


def update_profile(request, pk):
    id = int(pk)
    user_id = User.objects.get(id=pk)
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = user_id
            # Create a new product and set the user field
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect('user-list')

    context = {
        'form': form,
    }
    return render(request, 'profile.html', context)


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
    station_id = get_object_or_404(Station_admin, user=request.user)
    station = station_id.station
    form = PatientForm()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            user = request.user
            patient = form.save(commit=False)
            patient.user = user
            patient.care_centre = station
            patient.save()
            return redirect('patient-list')

    context = {
        'form': form,
    }

    return render(request, 'patient.html', context)


def addCampaign(request):
    station_id = get_object_or_404(Station_admin, user=request.user)
    station = station_id.station
    form = CampaignForm()
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            user = request.user
            campaign = form.save(commit=False)
            campaign.user = user
            campaign.care_centre = station
            campaign.save()
            return redirect('sta-camp')

    context = {
        'form': form,
    }

    return render(request, 'create_camp.html', context)

def addDiagnosis(request):
    form = DianosisForm()
    if request.method == 'POST':
        form = DianosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.save()
            return redirect('home')
    context = {
        'form': form
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
        'form': form
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
        'form': form
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
    admins = Station_admin.objects.filter(station=station_id)
    admins = [admin.user for admin in admins]
    profile = Profile.objects.all()

    context = {
        'station': station_id,
        'admins': admins,
        'profile': profile
    }
    return render(request, 'station_dash.html', context)


@login_required
@user_passes_test(is_user_admin)
def user_list(request):
    users_list = User.objects.all()
    profile = Profile.objects.all()
    context = {
        'users_list': users_list,
        'profile': profile
    }

    return render(request, 'users.html', context)


@login_required
@user_passes_test(is_user_admin)
def make_admin(request, id):
    station_id = get_object_or_404(Station, id=id)
    station_id = station_id.id
    s_id = Station.objects.get(id=station_id)
    form = MakeAdmin()
    if request.method == "POST":
        form = MakeAdmin(request.POST)
        if form.is_valid():
            station = s_id
            user = form.cleaned_data['user']

            if not User_admin.objects.filter(user=user).exists(): 
                form = form.save(commit=False)
                form.station = station
                form.save()
                return redirect('admin-dash')
            else:
                form.add_error('user', 'This user is already an admin.')
        
    context = {
        'form': form,
        'station_id': station_id
    }
    return render(request, 'make_admin.html', context)



def station_admin(request):
    info = get_object_or_404(Station_admin, user=request.user)
    station = info.station

    context = {
        'station': station,
    }

    return render(request, 'station_admin.html', context)

def CampList(request):
    
    campaigns = Campaign.objects.all()
    context = {
        'campaigns': campaigns,
        
    }

    return render(request, 'campaigns.html', context)

def Campaign_Info(request, pk):
    campaign = get_object_or_404(Campaign, id=pk)
    report = CampReport.objects.filter(campaign_id=campaign)

    context = {
        'campaign': campaign,
        'report': report
    }

    return render(request, 'campaign_info.html', context)

def Patient_List(request):
    info = get_object_or_404(Station_admin, user=request.user)
    station = info.station
    patient = Patient.objects.filter(care_centre=station)

    context = {
        'patient': patient,
        
    }

    return render(request, 'patient_list.html', context)

def Sta_Campaign(request):
    info = get_object_or_404(Station_admin, user=request.user)
    station = info.station
    campaign = Campaign.objects.filter(station=station)
    context = {
        'campaign': campaign
    }

    return render(request, 'station_campaigns.html', context)