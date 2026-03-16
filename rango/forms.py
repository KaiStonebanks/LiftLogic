from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    bench_press_max = forms.FloatField(min_value=10)
    squat_max = forms.FloatField(min_value=10)
    deadlift_max = forms.FloatField(min_value=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 
                  'bench_press_max', 'squat_max', 'deadlift_max']