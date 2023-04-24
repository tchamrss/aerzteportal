
from rest_framework import serializers
from django.contrib.auth.models import User

from portal.models import Doctor, Appointment, Patient



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username','email']

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    #user = UserSerializer(read_only=False)
    class Meta:
        model = Patient
        fields = ['id','first_name', 'last_name', 'doctor']

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id','title', 'description', 'created_at', 'date', 'doctor']
    """ def get_doctor_username(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    """

class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = ['id','speciality', 'title', 'user']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        instance = super().update(instance, validated_data)
        return instance