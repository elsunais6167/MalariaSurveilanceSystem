import email
from django.db import models
from sqlalchemy import null

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Station(models.Model):
    select = (
        ('Hospital', 'Hospital'),
        ('Clinic', 'Clinic'),
    )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=select) 
    gis_location = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    supervisor = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField(max_length=200)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Patient(models.Model):
    select = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=select)
    age = models.CharField(max_length=50)
    care_centre = models.ForeignKey(Station, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    family_size = models.IntegerField()
    no_of_children = models.IntegerField()
    sleeping_in_screen = models.BooleanField()
    use_of_insecticide = models.BooleanField()
    opening_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name