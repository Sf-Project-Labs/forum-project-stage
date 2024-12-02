from django.contrib import admin
from django.urls import path, include

from users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('', home, name='home')
]
