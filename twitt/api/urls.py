from django.urls import path
from twitt.api.views import Twitt_create_view, Twitt_delete_view, ReTwitt_create_view, Twitt_view

urlpatterns = [
    path('create/', Twitt_create_view.as_view(), name='Twitt_create_view'),
    path('delete/', Twitt_delete_view.as_view(), name='Twitt_delete_view'),
    path('retwitt/', ReTwitt_create_view.as_view(), name='ReTwitt_create_view'),
    path('list/', Twitt_view.as_view(), name='Twitt_view'),
]
