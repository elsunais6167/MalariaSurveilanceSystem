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
from .forms import CampReportForm, CampaignForm, CreateUserForm
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

@login_required
def household(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id
    house = None

    try:
        # Try to get an existing household
        house = Household.objects.get(patient_id=patient)
    except Household.DoesNotExist:
        pass

    if request.method == "POST":
        if house:  # if a household already exists, use it as instance for the form
            form = HouseholdForm(request.POST, instance=house)
        else:
            form = HouseholdForm(request.POST)

        if form.is_valid():
            house = form.save(commit=False)
            house.patient_id = patient
            house.user = request.user
            house.save()
            return redirect('patient-info', pk=pat_id )
    else:  # GET or other non-POST method
        if house:
            form = HouseholdForm(instance=house)
        else:
            form = HouseholdForm()

    context = {
        'form': form,
        'pat_id': pat_id,
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

def patient_prof(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    household = Household.objects.get(patient_id=patient)
    
    prevention = Preventive.objects.filter(patient_id=patient)
    diagnosis = Diagnosis.objects.filter(patient_id=patient)
    treatment = Treatment.objects.filter(patient_id=patient)
    morbidity = Morbidity.objects.filter(patient_id=patient)
    mortality = Mortality.objects.filter(patient_id=patient)

    pat_id = Patient.objects.get(id=pk)
    context = {
        'patient' : patient,
        'pat_id': pat_id,
        'household': household,
        'prevention': prevention,
        'diagnosis': diagnosis,
        'treatment': treatment,
        'morbidity': morbidity,
        'mortality': mortality,
    }

    return render(request, 'patient_prof.html', context)

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
            campaign.station = station
            campaign.save()
            return redirect('sta-camp')

    context = {
        'form': form,
    }

    return render(request, 'create_camp.html', context)

def Camp_Report(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    camp_id = campaign.id
    camp = Campaign.objects.get(id=camp_id)

    form = CampReportForm()
    if request.method == "POST":
        form = CampReportForm(request.POST)
        if form.is_valid():
            user = request.user
            campaign = form.save(commit=False)
            campaign.user = user
            campaign.campaign_id = camp
            campaign.save()
            return redirect('sta-camp')

    context = {
        'form': form,
        'camp_id': camp_id
    }

    return render(request, 'camp_report.html', context, )

def addDiagnosis(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id

    form = DianosisForm(initial={'pat_id': pat_id})
    if request.method == 'POST':
        form = DianosisForm(request.POST)
        if form.is_valid():
            user = request.user
            diagnosis = form.save(commit=False)
            diagnosis.user = user
            diagnosis.patient_id = patient
            diagnosis.save()
            return redirect('patient-info', pk=pat_id)
    context = {
        'form': form,
        'pat_id': pat_id
    }

    return render(request, 'diagnosis.html', context)


def addMorbidity(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id

    form = MorbidityForm(initial={'pat_id': pat_id})
    if request.method == 'POST':
        form = MorbidityForm(request.POST)
        if form.is_valid():
            user = request.user
            morbidity = form.save(commit=False)
            morbidity.user = user
            morbidity.patient_id = patient
            morbidity.save()
            return redirect('patient-info', pk=pat_id)

    context = {
        'form': form,
        'pat_id': pat_id
    }

    return render(request, 'morbidity.html', context)


def addMortality(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id

    form = MortalityForm(initial={'pat_id': pat_id})
    if request.method == 'POST':
        form = MortalityForm(request.POST)
        if form.is_valid():
            user = request.user
            mortality = form.save(commit=False)
            mortality.user = user
            mortality.patient_id = patient
            mortality.save()
            return redirect('patient-info', pk=pat_id)

    context = {
        'form': form,
        'pat_id': pat_id,
    }

    return render(request, 'mortality.html', context)


def addTreatment(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id

    form = TreatmentForm(initial={'pat_id': pat_id})
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            user = request.user
            treatment = form.save(commit=False)
            treatment.user = user
            treatment.patient_id = patient
            treatment.save()
            return redirect('patient-info', pk=pat_id)

    context = {
        'form': form,
        'pat_id': pat_id,
    }

    return render(request, 'treatment.html', context)


def addPreventive(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    pat_id = patient.id

    form = PreventionForm(initial={'pat_id': pat_id})
    if request.method == 'POST':
        form = PreventionForm(request.POST)
        if form.is_valid():
            user = request.user
            prevention = form.save(commit=False)
            prevention.user = user
            prevention.patient_id = patient
            prevention.save()
            return redirect('patient-info', pk=pat_id)

    context = {
        'form': form,
        'pat_id': pat_id,
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