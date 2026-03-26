from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 1RM values
    squat_1rm = models.IntegerField(null=True, blank=True)
    bench_1rm = models.IntegerField(null=True, blank=True)
    deadlift_1rm = models.IntegerField(null=True, blank=True)
    
    # Demographic details for leaderboard calculation
    bodyweight = models.FloatField(default=0.0)
    age = models.IntegerField(default=25)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')

    def __str__(self):
        return self.user.username

class LiftLog(models.Model):
    EXERCISE_CHOICES = [
        ('squat', 'Squat'),
        ('bench-press', 'Bench Press'),
        ('deadlift', 'Deadlift'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=50, choices=EXERCISE_CHOICES)
    weight = models.FloatField()
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise} - {self.weight}kg x {self.reps}"
    
    class Meta:
        ordering = ['-date']

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=50) # Same choices as above
    bodyweight = models.FloatField()
    weight = models.FloatField()
    reps = models.IntegerField()
    age = models.IntegerField()
    score = models.FloatField() # Calculated multiplier/score

    def __str__(self):
        return f"{self.user.username} - {self.exercise} Score: {self.score}"

    class Meta:
        ordering = ['-score']
