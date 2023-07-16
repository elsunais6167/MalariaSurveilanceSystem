from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('household/', views.household, name="household"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.loggingout, name='logout'),
    path('addStation/', views.addStation, name="addStation"),
    path('addpatient/', views.addPatient, name='addpatient'),
    path('add-diagnosis/', views.addDiagnosis, name='add-diagnosis'),
    path('add-morbidity/', views.addMorbidity, name='add-morbidity'),
    path('add-mortality/', views.addMortality, name='add-mortality'),
    path('add-treatment/', views.addTreatment, name='add-treatment'),
    path('add-prevention/', views.addPreventive, name='add-prevention'),
    path('admin-dash/', views.adminDash, name='admin-dash'),
    path('sta-dash/<str:pk>/', views.stationDash, name='sta-dashh'),
    path('add-user/', views.user_signup, name='add-user'),
    path('user-list/', views.user_list, name='user-list'),
    path('profile/<str:id>/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('make-admin/<str:id>/', views.make_admin, name='make-admin'),
    path('sta-admin/', views.station_admin, name='sta-admin'),
    path('camp-list', views.CampList, name='camp-list'),
    path('camp-info/<str:pk>/', views.Campaign_Info, name='camp-info'),
    path('patient-list', views.Patient_List, name='patient-list'),
    path('sta-camp', views.Sta_Campaign, name='sta-camp'),
    
]