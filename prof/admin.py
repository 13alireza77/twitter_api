from django.contrib import admin
from .models import UserProfile, Follow, Event

admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Event)
