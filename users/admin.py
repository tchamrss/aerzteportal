from django.contrib import admin
from users.models import Patient, Doctor, Appointment

""" class PatientsAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email') 
    list_display = ('user', 'first_name', 'last_name', 'email')"""
    
class DoctorsAdmin(admin.ModelAdmin):
    fields = ( 'user','title', 'speciality') 
    list_display = ('user' ,'title', 'speciality') 
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Appointment)