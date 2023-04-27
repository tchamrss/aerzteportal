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
from users.models import Patient, Appointment, Doctor
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model,authenticate
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appointments to be viewed or edited.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Holen Sie den angemeldeten Benutzer aus dem Anfrageobjekt
        user = self.request.user
        doctor_qs = Doctor.objects.filter(user=user)
        patient_qs = Patient.objects.filter(user=user)
        if doctor_qs.exists():
            doctor_ins = doctor_qs.first()
            return Appointment.objects.filter(doctor=doctor_ins)
        elif patient_qs.exists():
            patient_ins = patient_qs.first()
            return Appointment.objects.filter(patient=patient_ins)
        else:
            return Appointment.objects.none()   
    
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