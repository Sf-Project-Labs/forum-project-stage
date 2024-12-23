from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
