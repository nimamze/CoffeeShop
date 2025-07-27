from django.urls import path
from .views import UserProfileView, UpdateProfileView

urlpatterns = [
    path('user-profile/', UserProfileView.as_view(), name='UserProfile'),
    path('user-profile-update/', UpdateProfileView.as_view(), name='UserUpdateProfile'),
]
