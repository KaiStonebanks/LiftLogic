from django.contrib import admin
from .models import UserProfile, LiftLog, LeaderboardEntry

admin.site.register(UserProfile)
admin.site.register(LiftLog)
admin.site.register(LeaderboardEntry)
