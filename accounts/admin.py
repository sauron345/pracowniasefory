from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'role', 'created_date', 'is_active']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_editable = ['is_active']
    ordering = ('created_date',)
    filter_horizontal = ()
    list_filter = ['username', 'email', 'role', 'is_active', 'created_date']
    fieldsets = ()
