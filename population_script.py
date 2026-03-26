import os
import random
from datetime import timedelta
from django.utils import timezone

# Set up the Django environment before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftlogic_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rango.models import UserProfile, LiftLog

def add_user(username, password, email):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
    return user

def add_profile(user, age, bodyweight, gender, sq, bp, dl):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.age = age
    profile.bodyweight = bodyweight
    profile.gender = gender
    profile.squat_1rm = sq
    profile.bench_1rm = bp
    profile.deadlift_1rm = dl
    profile.save()
    return profile

def add_log(user, exercise, weight, reps, days_ago):
    date = timezone.now() - timedelta(days=days_ago)
    return LiftLog.objects.create(
        user=user,
        exercise=exercise,
        weight=weight,
        reps=reps,
        date=date
    )

def populate():
    print("Starting LiftLogic population script...")

    # Clear existing dummy data to avoid duplicates if run multiple times
    User.objects.exclude(is_superuser=True).delete()
    
    # 1. Create User: Alice (Powerlifter)
    u1 = add_user('alice', 'strength123', 'alice@liftlogic.com')
    add_profile(u1, 28, 65.0, 'female', 120, 70, 140)
    
    # Add logs for Alice
    exercises = ['squat', 'bench-press', 'deadlift']
    for i in range(7):
        ex = random.choice(exercises)
        weight = random.randint(50, 100)
        reps = random.randint(1, 8)
        add_log(u1, ex, weight, reps, days_ago=i)

    # 2. Create User: Bob (Beginner)
    u2 = add_user('bob', 'gymbro456', 'bob@liftlogic.com')
    add_profile(u2, 22, 80.0, 'male', 80, 60, 100)
    
    # Add logs for Bob
    for i in range(5):
        ex = random.choice(exercises)
        weight = random.randint(40, 70)
        reps = random.randint(5, 12)
        add_log(u2, ex, weight, reps, days_ago=i+1)

    # 3. Create User: Charlie (Advanced)
    u3 = add_user('charlie', 'heavyweight789', 'charlie@liftlogic.com')
    add_profile(u3, 35, 105.0, 'male', 220, 150, 260)
    
    # Add logs for Charlie
    for i in range(4):
        ex = random.choice(exercises)
        weight = random.randint(100, 200)
        reps = random.randint(1, 5)
        add_log(u3, ex, weight, reps, days_ago=i*2)

    print("Population script completed successfully. Built 3 users and generated sample lift histories.")

if __name__ == '__main__':
    print("Running population script...")
    populate()
