from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect

from portal.serializers import AppointmentSerializer, PatientSerializer, DoctorSerializer
from .models import Patient, Appointment, Doctor

# Create your views here.
class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = Patient.objects.all().order_by('-first_name')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appointments to be viewed or edited.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        # Hole den angemeldeten User aus dem Request-Objekt
        user = self.request.user

        # Hole den Doctor, dem der User gehört
        doctor = Doctor.objects.get(user=user)

        # Filtere die Appointments nach dem Doctor
        queryset = Appointment.objects.filter(doctor=doctor)

        return queryset

    
class DoctorViewSet(viewsets.ModelViewSet): 
    """
    API endpoint that allows doctors to be viewed or edited.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DoctorDeleteView(LoginRequiredMixin,generics.DestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PatientDeleteView(LoginRequiredMixin,generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentDeleteView(LoginRequiredMixin,generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')  # Hier 'home' durch die URL ersetzen, zu der Sie den Benutzer nach dem Ausloggen umleiten möchten