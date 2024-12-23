from django.contrib import admin

from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'business_plan', 'media_files', 'status',
                    'created_at', 'last_update', 'starting_at', 'finishing_at', 'start_up', 'investor')
    search_fields = ('name',)
