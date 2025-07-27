from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin, DetailView):
    
    model = CustomUser 
    template_name = 'accounts/user.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user
