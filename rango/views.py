from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, LiftLogForm, CalculatorForm
from .models import UserProfile, LiftLog, LeaderboardEntry
from .calculator import calculate

def register(request):
    """
    Handles user registration.
    Processes both the base UserForm and custom UserProfileForm to create a new authenticated user session.
    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            login(request, user)
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

@login_required
def home(request):
    """
    Renders the main dashboard index page.
    Authentication is required to view this dashboard.
    """
    return render(request, 'rango/index.html')

@login_required
def profile(request):
    """
    Displays the user profile including their historical logs and 1 Rep Maxes.
    Allows for inline editing of 1RMs and submitting past logs directly from the profile page.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_1rm':
            squat_1rm = request.POST.get('squat_1rm')
            bench_1rm = request.POST.get('bench_1rm')
            deadlift_1rm = request.POST.get('deadlift_1rm')
            
            user_profile.squat_1rm = int(squat_1rm) if squat_1rm else None
            user_profile.bench_1rm = int(bench_1rm) if bench_1rm else None
            user_profile.deadlift_1rm = int(deadlift_1rm) if deadlift_1rm else None
            user_profile.save()
            return redirect('profile')
        elif action == 'add_log':
            form = LiftLogForm(request.POST)
            if form.is_valid():
                log = form.save(commit=False)
                log.user = request.user
                log.save()
                return redirect('profile')
    
    # 7-day Lift History
    seven_days_ago = timezone.now() - timedelta(days=7)
    logs = LiftLog.objects.filter(user=request.user, date__gte=seven_days_ago).order_by('-date')
    
    log_form = LiftLogForm()
    
    return render(request, 'rango/profile.html', {
        'user_profile': user_profile,
        'logs': logs,
        'log_form': log_form
    })

@login_required
def delete_log(request, log_id):
    """
    Standard endpoint to remove a LiftLog.
    Returns the user to the profile page after deletion.
    """
    log = get_object_or_404(LiftLog, id=log_id, user=request.user)
    if request.method == 'POST':
        log.delete()
    return redirect('profile')

@login_required
def ajax_delete_log(request, log_id):
    """
    AJAX endpoint for deleting a lift log dynamically without full page refresh.
    Returns status: success or status: error JSON.
    """
    if request.method == 'POST':
        log = get_object_or_404(LiftLog, id=log_id, user=request.user)
        log.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def leaderboard(request):
    """
    Displays the Smart Strength Calculator interface.
    Accepts generic weights and body metrics to estimate a user's relative strength multiplier
    and classifies them across worldwide fitness standards without saving to the database.
    """
    calc_result = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            try:
                calc_result = calculate(
                    exercise_slug=form.cleaned_data['exercise'],
                    weight=form.cleaned_data['weight'],
                    reps=form.cleaned_data['reps'],
                    bodyweight=form.cleaned_data['bodyweight'],
                    gender=form.cleaned_data['gender']
                )
            except ValueError:
                pass
    else:
        form = CalculatorForm()

    return render(request, 'rango/leaderboard.html', {'form': form, 'calc_result': calc_result})

@login_required
def workout(request, exercise_slug):
    """
    Core logic for displaying the 3-week Smolov Jr. progression table.
    Takes the user's 1RM for the requested exercise and generates custom daily workout targets.
    Handles logging of completed lifts and dynamic feedback generation based on perceived difficulty.
    """
    # Retrieve the user profile for 1RM and demographic data
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Get the 1RM based on the selected exercise
    one_rm = 0.0
    if exercise_slug == 'squat':
        one_rm = user_profile.squat_1rm or 0.0
    elif exercise_slug == 'bench-press':
        one_rm = user_profile.bench_1rm or 0.0
    elif exercise_slug == 'deadlift':
        one_rm = user_profile.deadlift_1rm or 0.0

    # Smolov Jr Program logic (3 weeks)
    program = [
        {'day': 1, 'sets': 6, 'reps': 6, 'percentage': 70},
        {'day': 2, 'sets': 7, 'reps': 5, 'percentage': 75},
        {'day': 3, 'sets': 8, 'reps': 4, 'percentage': 80},
        {'day': 4, 'sets': 10, 'reps': 3, 'percentage': 85},
    ]

    for day in program:
        raw_weight = one_rm * (day['percentage'] / 100.0)
        base_weight = round(raw_weight / 2.5) * 2.5
        day['week1'] = base_weight
        day['week2'] = base_weight + 2.5
        day['week3'] = base_weight + 5.0

    # Handle form submission
    feedback_msg = None
    if request.method == 'POST':
        form = LiftLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            # Ensure the exercise matches the current page
            log.exercise = exercise_slug
            log.save()
            
            # Predict new 1RM and update Leaderboard
            try:
                calc_result = calculate(
                    exercise_slug=exercise_slug, 
                    weight=log.weight, 
                    reps=log.reps, 
                    bodyweight=user_profile.bodyweight, 
                    gender=user_profile.gender
                )
                
                # Check for existing LeaderboardEntry for this user and exercise
                entry, created = LeaderboardEntry.objects.get_or_create(
                    user=request.user,
                    exercise=exercise_slug,
                    defaults={
                        'bodyweight': user_profile.bodyweight,
                        'weight': log.weight,
                        'reps': log.reps,
                        'age': user_profile.age,
                        'score': calc_result.multiplier
                    }
                )
                
                # If existing score is lower, update the entry!
                if not created and calc_result.multiplier > entry.score:
                    entry.bodyweight = user_profile.bodyweight
                    entry.weight = log.weight
                    entry.reps = log.reps
                    entry.age = user_profile.age
                    entry.score = calc_result.multiplier
                    entry.save()
                    
            except ValueError as e:
                pass # Issue with calculator

            feedback_weight = request.POST.get('feedback', 'moderate')
            if feedback_weight == 'easy':
                feedback_msg = "Great job! Consider increasing your reps by 1 or your working weight by 2.5kg."
            elif feedback_weight == 'difficult':
                feedback_msg = "Tough session. Consider decreasing your reps by 1 or your working weight by 2.5kg."
            else:
                feedback_msg = "Solid work! Maintain your current programmed weights."

            form = LiftLogForm(initial={'exercise': exercise_slug})
    else:
        form = LiftLogForm(initial={'exercise': exercise_slug})

    return render(request, 'rango/workout.html', {
        'exercise_slug': exercise_slug,
        'program': program,
        'one_rm': one_rm,
        'form': form,
        'feedback_msg': feedback_msg
    })

def about_us(request):
    return render(request, 'rango/about_us.html')

def contact_us(request):
    return render(request, 'rango/contact_us.html')

def guides(request):
    return render(request, 'rango/guides.html')
