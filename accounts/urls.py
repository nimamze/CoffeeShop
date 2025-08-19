from django.urls import path, include

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
    path("api/v1/", include("accounts.api.v1.urls")),
]
