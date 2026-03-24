from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rango/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('program/bench-press/', views.bench_press_program, name='bench_press'),
    path('program/squat/', views.squat_program, name='squat'),
    path('program/deadlift/', views.deadlift_program, name='deadlift'),
    path('profile/', views.profile, name='profile'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('faqs/', views.faqs, name='faqs'),
]
