from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('household/', views.household, name="household"),
    path('addStation/', views.addStation, name="addStation"),
    path('addpatient/', views.addPatient, name='addpatient'),
    path('add-diagnosis/', views.addDiagnosis, name='add-diagnosis'),
]