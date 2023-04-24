from django.conf import settings
from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Doctor(models.Model):
    TITLES = [
            ("Dr", "Dr"),
            ( "Prof.Dr", "Prof.Dr"),
            ("Dr.rer.nat", "Dr.rer.nat"),
        ]
    SPECIALITIES = [
            ("Allgemeinmedizin", "Allgemeinmedizin"),
            ("Radiologe", "Radiologe"),
            ("Hautarzt", "Hautarzt"),
        ]
    speciality = models.CharField(max_length=20, choices=SPECIALITIES)
    title = models.CharField(max_length=50, choices=TITLES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} {self.user.first_name} {self.user.last_name}"

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    @property
    def creator_name(self):
        return f"{self.doctor.title} {self.doctor.user.first_name} {self.doctor.user.last_name}"

class Appointment(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    created_at =  models.DateField(default=date.today)
    date =  models.DateField(default=date.today)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    