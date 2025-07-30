from django.contrib.auth.views import LoginView
from django.db.models.base import Model as Model
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'
    

class SignUpView(CreateView):

    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  


class ProfileView(LoginRequiredMixin,DetailView):

    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
