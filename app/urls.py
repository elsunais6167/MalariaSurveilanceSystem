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
]