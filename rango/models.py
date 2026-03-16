from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bench_press_max = models.FloatField()
    squat_max = models.FloatField()
    deadlift_max = models.FloatField()

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    sets = models.IntegerField()
    reps = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=[
        ('too-hard', 'Too Hard'),
        ('too-easy', 'Too Easy'),
        ('all-good', 'All Good'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)