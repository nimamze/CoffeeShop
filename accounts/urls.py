from django.urls import path
from .views import UserProfileView, UpdateProfileView,UserFavoritesView

urlpatterns = [
    path('user-profile/', UserProfileView.as_view(), name='profile'),
    path('user-profile-update/', UpdateProfileView.as_view(), name='user_update'),
    path('user-favorites/', UserFavoritesView.as_view(), name='favorites'),
]
