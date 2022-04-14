"""config URL Configuration

"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_page_app.urls')),
    path('users/', include('users_app.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users_app/reset_password.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users_app/reset_password_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users_app/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users_app/reset_password_complet.html'),
         name='password_reset_complete'),
    path('management/', include('management_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
