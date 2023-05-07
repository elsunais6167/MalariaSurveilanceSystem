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

class Diagnosis(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    opening_date = models.DateField(auto_now_add=True, null=True)
    mode_choices = (
        ('New Diagnosis', 'New Diagnosis'),
        ('Follow Up Diangosis', 'Follow Up Diagnosis'),
    )
    mode_of_diagnosis = models.CharField(max_length=50, choices=mode_choices)
    select = (
        ('RDT', 'RDT'),
        ('Microscopy', 'Microscopy'),
        ('PCR', 'PCR'),
    )
    dianosis_type = models.CharField(max_length=50, choices=select)
    result_choice = (
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
    )
    results = models.CharField(max_length=50, choices=result_choice)
    malaria_choices = (
        ('P. falciparum', 'P. falciparum'),
        ('P. vivae', 'P. vivae'),
        ('P. ovale', 'P. ovale'),
        ('P. malariae', 'P. malariae'),
    )
    malaria_type = models.CharField(max_length=50, choices=malaria_choices)
    parasitemia_load = models.CharField(max_length=50)
    comment = models.TextField(max_length=5000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient_id.name

class Morbidity(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    severity_choice = (
        ('Mild (uncomplecated)', 'Mild (uncomplecated)'),
        ('Moderate (uncomplecated)', 'Moderate (uncomplecated)'),
        ('Severe (complecated)', 'Severe (complecated)'),
    )
    severity = models.CharField(max_length=50, choices=severity_choice)
    mode_choices = (
        ('Hospitilized', 'Hospitalized'),
        ('Home Treatment', 'Home Treatment'),
    )
    mode_of_admission = models.CharField(max_length=50, choices=mode_choices)
    comment = models.TextField(max_length=5000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient_id.name

class Treatment(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treat_choice = (
        ('ACTs', 'ACTs'),
        ('Non ACTs', 'Non ACTs'),
        ('Others', 'Others'),
    )
    treatment_type = models.CharField(max_length=50, choices=treat_choice)
    period = (
        ('3 Days', '3 Days'),
        ('7 Days', '7 Days'),
        ('14 Days', '14 Days'),
    )
    treatment_period = models.CharField(max_length=50, choices=period)
    further_treatment = models.BooleanField()
    follow_up = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient_id.name
    
class Mortality(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    select = (
        ('Mortality', 'Mortality'),
        ('Healed/Discharge', 'Healed/Discharge'),
    )
    status = models.CharField(max_length=50)
    date = models.DateField()
    date_created = models.DateField(auto_now_add=True) 
