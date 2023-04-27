from django.conf import settings
from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
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
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='doctor_groups',  # Change related name for reverse accessor
        related_query_name='doctor_group',
        to='auth.Group',
    )
    user_permissions = models.ManyToManyField(
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='doctor_user_permissions',  # Change related name for reverse accessor
        related_query_name='doctor_user_permission',
        to='auth.Permission',
    )
    
    class Meta:
        verbose_name='doctor'
        verbose_name_plural='doctors'
    """ def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" """

class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    groups = models.ManyToManyField(
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='patient_groups',  # unique related name
        related_query_name='patient_group',
        to='auth.Group',
    )
    user_permissions = models.ManyToManyField(
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='patient_user_permissions',  # unique related name
        related_query_name='patient_user_permission',
        to='auth.Permission',
    )
      
    class Meta:
        verbose_name='patient'
        verbose_name_plural='patients'
    

class Appointment(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    created_at = models.DateField(default=date.today)
    date = models.DateField(default=date.today)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments_as_patient')
