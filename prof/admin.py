from django.contrib import admin
from .models import UserProfile, Follow, UnFollow

admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(UnFollow)
