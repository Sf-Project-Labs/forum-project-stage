from django.contrib import admin
from .models import StartUpProfile


@admin.register(StartUpProfile)
class StartUpAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'legal_name', 'email', 'phone_number', 'region',
                    'industry_type', 'user', 'project_information')
    search_fields = ('company_name', 'legal_name')
