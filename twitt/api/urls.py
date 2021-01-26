from django.urls import path
from twitt.api.views import Twitt_create_view, Twitt_delete_view, ReTwitt_create_view, Twitt_view, Likes_view, \
    Like_create_view, Comment_create_view, Get_twitt, Get_top_Hashtags

urlpatterns = [
    path('create/', Twitt_create_view.as_view(), name='Twitt_create_view'),
    path('delete/', Twitt_delete_view.as_view(), name='Twitt_delete_view'),
    path('retwitt/', ReTwitt_create_view.as_view(), name='ReTwitt_create_view'),
    path('list/', Twitt_view.as_view(), name='Twitt_view'),
    path('like/', Like_create_view.as_view(), name='Like_create_view'),
    path('likes/users', Likes_view.as_view(), name='Likes_view'),
    path('comment/create', Comment_create_view.as_view(), name='Comment_create_view'),
    path('get/<int:pk>', Get_twitt.as_view(), name='Get_twitt'),
    path('top_hashtags/', Get_top_Hashtags.as_view(), name='Get_top_Hashtags'),
]
