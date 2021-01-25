from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from prof.api.views import RegisterApi, Logout_view, Follow_create_view, Following_view, \
    Follower_view, UnFollow_view

urlpatterns = [
    path('register', RegisterApi.as_view(), name='register'),
    path('logout/', Logout_view.as_view(), name='logout', ),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/', Follow_create_view.as_view(), name='Follow_create_view'),
    path('unfollow/', UnFollow_view.as_view(), name='Follow_delete_view'),
    path('follower/list', Follower_view.as_view(), name='Follower_view'),
    path('following/list', Following_view.as_view(), name='Following_view'),
]
