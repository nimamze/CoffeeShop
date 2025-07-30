from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UpdateProfileView,
    UserFavoritesView,
    ProfileView,
    CustomLoginView,
    SignUpView
)

urlpatterns = [
    path('user-profile/', ProfileView.as_view(), name='profile'),
    path('user-profile-update/', UpdateProfileView.as_view(), name='user_update'),
    path('user-favorites/', UserFavoritesView.as_view(), name='favorites'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
