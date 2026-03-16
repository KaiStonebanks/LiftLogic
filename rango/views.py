from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                bench_press_max=form.cleaned_data['bench_press_max'],
                squat_max=form.cleaned_data['squat_max'],
                deadlift_max=form.cleaned_data['deadlift_max']
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'rango/register.html', {'form': form})

@login_required
def home(request):
    profile = request.user.userprofile
    context = {
        'bench_max': profile.bench_press_max,
        'squat_max': profile.squat_max,
        'deadlift_max': profile.deadlift_max,
    }
    return render(request, 'rango/home.html', context)

@login_required
def bench_press_program(request):
    profile = request.user.userprofile
    program = generate_smolov_program(profile.bench_press_max)
    return render(request, 'rango/program.html', {
        'exercise_name': 'Bench Press',
        'one_rep_max': profile.bench_press_max,
        'program': program
    })

@login_required
def squat_program(request):
    profile = request.user.userprofile
    program = generate_smolov_program(profile.squat_max)
    return render(request, 'rango/program.html', {
        'exercise_name': 'Squat',
        'one_rep_max': profile.squat_max,
        'program': program
    })

@login_required
def deadlift_program(request):
    profile = request.user.userprofile
    program = generate_smolov_program(profile.deadlift_max)
    return render(request, 'rango/program.html', {
        'exercise_name': 'Deadlift',
        'one_rep_max': profile.deadlift_max,
        'program': program
    })

@login_required
def profile(request):
    profile = request.user.userprofile
    context = {
        'bench_max': profile.bench_press_max,
        'squat_max': profile.squat_max,
        'deadlift_max': profile.deadlift_max,
    }
    return render(request, 'rango/profile.html', context)

def generate_smolov_program(one_rep_max):
    weeks = {
        'week1': [
            {'day': 'Monday', 'sets': 6, 'reps': 6, 'percentage': 70},
            {'day': 'Wednesday', 'sets': 7, 'reps': 5, 'percentage': 75},
            {'day': 'Friday', 'sets': 8, 'reps': 4, 'percentage': 80},
            {'day': 'Saturday', 'sets': 10, 'reps': 3, 'percentage': 85},
        ],
        'week2': [
            {'day': 'Monday', 'sets': 6, 'reps': 6, 'percentage': 70},
            {'day': 'Wednesday', 'sets': 7, 'reps': 5, 'percentage': 75},
            {'day': 'Friday', 'sets': 8, 'reps': 4, 'percentage': 80},
            {'day': 'Saturday', 'sets': 10, 'reps': 3, 'percentage': 85},
        ],
        'week3': [
            {'day': 'Monday', 'sets': 6, 'reps': 6, 'percentage': 75},
            {'day': 'Wednesday', 'sets': 7, 'reps': 5, 'percentage': 80},
            {'day': 'Friday', 'sets': 8, 'reps': 4, 'percentage': 85},
            {'day': 'Saturday', 'sets': 10, 'reps': 3, 'percentage': 90},
        ],
        'week4': [
            {'day': 'Monday', 'sets': 6, 'reps': 6, 'percentage': 75},
            {'day': 'Wednesday', 'sets': 7, 'reps': 5, 'percentage': 80},
            {'day': 'Friday', 'sets': 8, 'reps': 4, 'percentage': 85},
            {'day': 'Saturday', 'sets': 10, 'reps': 3, 'percentage': 90},
        ],
    }
    
    # Calculate weights for each workout
    for week_name, workouts in weeks.items():
        for workout in workouts:
            workout['weight'] = round((one_rep_max * workout['percentage']) / 100)
    
    return weeks