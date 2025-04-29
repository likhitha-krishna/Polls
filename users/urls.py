from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = "users"
urlpatterns = [
    path("register/",UserRegistrationView.as_view(),name="user_register"),
    path("token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("token/verify/",TokenVerifyView.as_view(),name="token_verify"),
] 
