from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from prof.api.views import RegisterApi, Logout_view, Follow_create_view, Following_view, \
    Follower_view, UnFollow_view, Get_My, Get_Profie, ChangePasswordView, UpdateProfileView, GetEvent

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('logout/', Logout_view.as_view(), name='logout', ),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/', Follow_create_view.as_view(), name='Follow_create_view'),
    path('unfollow/', UnFollow_view.as_view(), name='Follow_delete_view'),
    path('follower/list/<str:username>', Follower_view.as_view(), name='Follower_view'),
    path('following/list/<str:username>', Following_view.as_view(), name='Following_view'),
    path('myprofile/', Get_My.as_view(), name='Get_My'),
    path('profile/<str:username>', Get_Profie.as_view(), name='Get_Profie'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('event/', GetEvent.as_view(), name='GetEvent'),
]
