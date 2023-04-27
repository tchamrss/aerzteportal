from .models import Patient
from django.contrib.auth.forms import UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = '__all__'