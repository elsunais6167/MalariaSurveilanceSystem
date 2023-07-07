from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('household/', views.household, name="household"),
    path('addStation/', views.addStation, name="addStation"),
    path('addpatient/', views.addPatient, name='addpatient'),
    path('add-diagnosis/', views.addDiagnosis, name='add-diagnosis'),
    path('add-morbidity/', views.addMorbidity, name='add-morbidity'),
    path('add-mortality/', views.addMortality, name='add-mortality'),
    path('add-treatment/', views.addTreatment, name='add-treatment'),
    path('add-prevention/', views.addPreventive, name='add-prevention'),
    path('admin-dash/', views.adminDash, name='admin-dash'),
    path('sta-dash/<str:pk>/', views.stationDash, name='sta-dash'),
    path('user-dash/', views.UserDash, name="user-dash"),
    path('add-user/', views.user_signup, name='add-user'),
    path('user-list/', views.user_list, name='user-list'),
    path('make-admin/<str:pk>/', views.make_admin, name='make-admin'),
    path('sta-admin/', views.station_admin, name='sta-admin'),
] 