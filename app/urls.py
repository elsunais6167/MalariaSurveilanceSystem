from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('household/', views.household, name="household"),
    path('addStation/', views.addStation, name="addStation")
]