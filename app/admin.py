from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Station)
admin.site.register(Patient)
admin.site.register(Diagnosis)
admin.site.register(Treatment)
admin.site.register(Morbidity)
admin.site.register(Mortality)
