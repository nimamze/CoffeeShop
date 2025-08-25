from django.urls import path
from .views import SignUpApi, SignUpConfirmApi, ProfileApi, LogoutVIewApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair_api"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh_api"),
    path("sign-up/", SignUpApi.as_view(), name="sign_up_api"),
    path("sign-up-confirm/", SignUpConfirmApi.as_view(), name="sign_up_confirm_api"),
    path("profile/", ProfileApi.as_view(), name="profile_api"),
    path("log-out/", LogoutVIewApi.as_view(), name="log_out_api")
]
