"""config URL Configuration

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_page_app.urls')),
    path('users/', include('users_app.urls')),
]
