from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['phone', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ("is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets
    search_fields = ("username", "email")
    ordering = ["phone"]
