from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from shop.models import Favorite, Product, Order
from django.contrib.auth import logout


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("profile")


def logout_view(request):
    logout(request)
    return redirect("login")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/UserProfile.html"
    context_object_name = "user_profile"

    def get_object(self):
        return self.request.user


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["first_name", "last_name", "email", "image", "phone"]
    template_name = "accounts/UserUpdateProfile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user


class UserFavoritesView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = "accounts/UserFavorites.html"
    context_object_name = "user_favorites"

    def get_queryset(self):
        return Favorite.objects.filter(customer=self.request.user)


def add_to_favorites(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Favorite.objects.get_or_create(customer=request.user, product=product)
    return redirect("favorites")


class UserOrdersView(ListView):
    model = Order
    template_name = "accounts/user_orders.html"
    context_object_name = "user_orders"

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class UserOrderDetailView(DetailView):
    model = Order
    template_name = "accounts/user_order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = self.object.items.all()  # type: ignore # related_name='items'
        return context
