from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView , ListView
from .models import CustomUser
from shop.models import Favorite
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin, DetailView):

    model = CustomUser
    template_name = 'accounts/UserProfile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class UpdateProfileView(LoginRequiredMixin, UpdateView):

    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'image', 'phone']
    template_name = 'accounts/UserUpdateProfile.html'
    success_url = reverse_lazy('UserProfile')

    def get_object(self):
        return self.request.user

class UserFavoritesView(LoginRequiredMixin,ListView):
    
    model =  Favorite
    template_name = 'accounts/UserFavorites.html'
    context_object_name = 'user_favorites'
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
