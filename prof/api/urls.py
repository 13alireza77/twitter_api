from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from prof.api.views import RegisterApi, Logout_view

urlpatterns = [
    path('register', RegisterApi.as_view()),
    path('logout/', Logout_view.as_view(), name='logout', ),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
