import email
from django.db import models
from sqlalchemy import null

from django.contrib.auth.models import User

# Create your models here.
class User_admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Station(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    select = (
        ('Hospital', 'Hospital'),
        ('Clinic', 'Clinic'),
        ('Laboratory', 'Laboratory'),
    )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=select) 
    gis_location = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    supervisor = models.TextField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField(max_length=200)
    date_created = models.DateField()

    def __str__(self):
        return self.name

class Station_admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    select = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=select)
    age = models.CharField(max_length=50)
    care_centre = models.ForeignKey(Station, on_delete=models.CASCADE)
    address = models.TextField(max_length=200)
    opening_date = models.DateField()

    def __str__(self):
        return self.name

class Household(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.OneToOneField(Patient, on_delete=models.CASCADE, unique=True)
    family_size = models.IntegerField()
    no_of_children = models.IntegerField()
    sleeping_in_screen = models.BooleanField()
    drainage = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    drainage_system = models.CharField(max_length=50, choices=drainage)

    def __str__(self):
        return self.patient_id.name

class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    opening_date = models.DateField(null=True)
    mode_choices = (
        ('New Diagnosis', 'New Diagnosis'),
        ('Follow Up Diangosis', 'Follow Up Diagnosis'),
    )
    mode_of_diagnosis = models.CharField(max_length=50, choices=mode_choices)
    select = (
        ('Physical Examination', 'Physical Examination'),
        ('RDT', 'RDT'),
        ('Microscopy', 'Microscopy'),
        ('PCR', 'PCR'),
        ('Combination', 'Combination'),
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
    date_created = models.DateField()

    def __str__(self):
        return self.patient_id.name

class Morbidity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    date_created = models.DateField()

    def __str__(self):
        return self.patient_id.name

class Treatment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    follow_up = models.BooleanField()
    further_treatment = models.BooleanField()
    comment = models.TextField(max_length=5000)
    date_created = models.DateField()

    def __str__(self):
        return self.patient_id.name
    
class Mortality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    select = (
        ('Mortality', 'Mortality'),
        ('Healed/Discharge', 'Healed/Discharge'),
    )
    status = models.CharField(max_length=50, choices=select)
    date = models.DateField()
    date_created = models.DateField() 

class Preventive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    use_of_mosquito_net = models.BooleanField()
    use_of_insecticide = models.BooleanField()
    use_of_repellant = models.BooleanField()
    days = (
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('6 Months', '6 Months'),
        ('Annually', 'Annually'),
    )
    indoor_residual = models.CharField(max_length=50, choices=days)
    date_reported = models.DateField()
    
    def __str__(self):
        return self.patient_id.name

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = (
        ('Mass Screening', 'Mass Screening'),
        ('Community Camp', 'Community Camp'),
    )
    campaign_type = models.CharField(max_length=50, choices=type)
    select = (
        ('Governmental', 'Governmental'),
        ('Non-Governmental Organisation', 'Non-Governmental Organisation'),
        ('Private Organisation', 'Private Organisation'),
        ('Community Initiative', 'Community Initiative'), 
    )
    name = models.CharField(max_length=50)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=select) 
    gis_location = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    supervisor = models.TextField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField(max_length=200)
    date_created = models.DateField()

    def __str__(self):
        return self.name

class CampReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    screened = models.IntegerField()
    treated = models.IntegerField()
    referral = models.IntegerField()
    date_created = models.DateField()

    def __str__(self):
        return self.campaign_id.name
