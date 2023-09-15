import json
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.db import models
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.urls import reverse

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
    stations = Station.objects.count()
    campaigns = Campaign.objects.count()
    station1 = Station.objects.all()

    pat_count1 = Diagnosis.objects.count()
    pat_count2 = CampReport.objects.aggregate(total_screened=Sum('screened'))['total_screened']
    total_screened = pat_count1 + pat_count2

    pos_count1 = CampReport.objects.aggregate(total_treated=Sum('treated'))['total_treated']
    pos_count2 = CampReport.objects.aggregate(total_referral=Sum('referral'))['total_referral']
    pos_count3 = Diagnosis.objects.filter(results='Positive').count()
    pos_cases = pos_count1 + pos_count2 + pos_count3

    stations_map = Station.objects.all()
    markers = []
    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        screened_count = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened=Sum('screened'))['total_screened']
        treated_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated=Sum('treated'))['total_treated']
        refer_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral=Sum('referral'))['total_referral']
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    context = {
        'stations': stations,
        'campaigns': campaigns,
        'markers_json': json.dumps(markers),
        'pat_count': total_screened,
        'pos_cases': pos_cases,
        'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'index.html', context)

   
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

    return render(request, 'login.html', {'error_message': error_message, 'login_error': login_error})


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
    
    try:
        household = Household.objects.get(patient_id=patient)
    except Household.DoesNotExist:
        household = None
        
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
    stations = Station.objects.count()
    campaigns = Campaign.objects.count()
    station1 = Station.objects.all()

    pat_count1 = Diagnosis.objects.count()
    pat_count2 = CampReport.objects.aggregate(total_screened=Sum('screened'))['total_screened']
    total_screened = pat_count1 + pat_count2

    pos_count1 = CampReport.objects.aggregate(total_treated=Sum('treated'))['total_treated']
    pos_count2 = CampReport.objects.aggregate(total_referral=Sum('referral'))['total_referral']
    pos_count3 = Diagnosis.objects.filter(results='Positive').count()
    pos_cases = pos_count1 + pos_count2 + pos_count3

    stations_map = Station.objects.all()
    markers = []
    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        screened_count = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened=Sum('screened'))['total_screened']
        treated_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated=Sum('treated'))['total_treated']
        refer_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral=Sum('referral'))['total_referral']
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    context = {
        'stations': stations,
        'campaigns': campaigns,
        'markers_json': json.dumps(markers),
        'pat_count': total_screened,
        'pos_cases': pos_cases,
        'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'admin_dash.html', context)

@login_required
@user_passes_test(is_user_admin)
def station_list(request):
    station_list = Station.objects.all()

    context = {
        'station_list': station_list,

    }

    return render(request, 'station_list.html', context)

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

def Campaign_Public(request, pk):
    campaign = get_object_or_404(Campaign, id=pk)
    reports = CampReport.objects.filter(campaign_id=campaign).order_by('-date_created')  # Assuming date_created exists and you want the newest entries first

    paginator = Paginator(reports, 5)  # Show 5 reports per page

    page = request.GET.get('page')  # Get the 'page' parameter from the URL
    report = paginator.get_page(page)

    screened_count = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened=Sum('screened'))['total_screened']
    treated_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated=Sum('treated'))['total_treated']
    refer_cases = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral=Sum('referral'))['total_referral']


    context = {
        'campaign': campaign,
        'report': report,
        'screened_count': screened_count,
        'treated_cases': treated_cases,
        'refer_cases': refer_cases,
    }

    return render(request, 'camp_public.html', context)

def Station_Public(request, pk):
    station = get_object_or_404(Station, id=pk)
    patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
    positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

    daily_counts = Diagnosis.objects.filter(
    patient_id__care_centre=station
    ).annotate(
        year=ExtractYear('date_created'),
        month=ExtractMonth('date_created'),
        day=ExtractDay('date_created')
    ).values('year', 'month', 'day').annotate(
        total_count=Count('id'),
        positive_count=Count('id', filter=models.Q(results='Positive'))
    ).order_by('year', 'month', 'day')
    
    paginator = Paginator(daily_counts, 5)  # Show 5 daily_counts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'station': station,
        'patients_count': patients_count,
        'positive_cases': positive_cases,
        'daily_counts': daily_counts,
        'page_obj': page_obj,
    }

    return render(request, 'station_public.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST.get('search')
        
        result = Campaign.objects.filter(name__contains=searched)
        result2 = Station.objects.filter(name__contains=searched)
        
        if result.exists():
            campaign = result.first() 
            return redirect('camp-public', pk=campaign.id)
        
        
        elif result2.exists():
            station = result2.first() 
            return redirect('sta-public', pk=station.id)

        else:
            error_message = 'There is no station or campaign with the name "{}".'.format(searched)
            return render(request, 'index.html', {'error_message': error_message, 'searched': searched })
