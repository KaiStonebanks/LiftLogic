from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile, LiftLog

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('squat_1rm', 'bench_1rm', 'deadlift_1rm')

class CalculatorForm(forms.Form):
    EXERCISE_CHOICES = [
        ('squat', 'Squat'),
        ('bench-press', 'Bench Press'),
        ('deadlift', 'Deadlift'),
        ('overhead-press', 'Overhead Press'),
        ('barbell-row', 'Barbell Row'),
    ]
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    
    exercise = forms.ChoiceField(choices=EXERCISE_CHOICES)
    weight = forms.FloatField(label='Weight Lifted (kg)')
    reps = forms.IntegerField(label='Reps')
    bodyweight = forms.FloatField(label='Bodyweight (kg)')
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

class LiftLogForm(forms.ModelForm):
    class Meta:
        model = LiftLog
        fields = ('exercise', 'weight', 'reps')
