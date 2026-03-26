from django.urls import path
from rango import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('sign-up/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rango/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('workout/<slug:exercise_slug>/', views.workout, name='workout'),
    path('delete_log/<int:log_id>/', views.delete_log, name='delete_log'),
    path('ajax/delete_log/<int:log_id>/', views.ajax_delete_log, name='ajax_delete_log'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('guides/', views.guides, name='guides'),
]
