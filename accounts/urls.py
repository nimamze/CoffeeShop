from django.urls import path

from .views import (
    UpdateProfileView,
    UserFavoritesView,
    ProfileView,
    CustomLoginView,
    SignUpView,
    UserOrdersView,
    UserOrderDetailView,
    add_to_favorites,
    logout_view,
)

from accounts.api_views import SignUpApi, SignUpConfirmApi, ProfileApi



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"

urlpatterns = [
    path("user-profile/", ProfileView.as_view(), name="profile"),
    path("user-profile-update/", UpdateProfileView.as_view(), name="user_update"),
    path("user-favorites/", UserFavoritesView.as_view(), name="favorites"),
    path("add-to-favorites/<int:pk>/", add_to_favorites, name="add_to_favorites"),
    path("user-orders/", UserOrdersView.as_view(), name="orders"),
    path("user-orders/<int:pk>/", UserOrderDetailView.as_view(), name="order_detail"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("api/sign-up/", SignUpApi.as_view(), name="sign_up_api"),
    path(
        "api/sign-up-confirm/", SignUpConfirmApi.as_view(), name="sign_up_confirm_api"
    ),
    path("api/profile/", ProfileApi.as_view(), name="profile_api"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair_api"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh_api"),
]
