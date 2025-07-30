from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
]