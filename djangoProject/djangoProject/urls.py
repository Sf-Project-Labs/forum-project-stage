from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('health/', health_check, name='health-check'),
    path('profiles/', include('profiles.urls')),
]
