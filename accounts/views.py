from django.shortcuts import render
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import CustomUser



class CustomLoginView(LoginView) :
    template_name = 'accounts/login.html'
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  


class ProfileView(ListView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'