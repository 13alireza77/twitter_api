from django.contrib import admin
from .models import Twitt, Hashtag, Retwitt, Like

admin.site.register(Twitt)
admin.site.register(Retwitt)
admin.site.register(Hashtag)
admin.site.register(Like)
