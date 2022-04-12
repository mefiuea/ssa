from django.urls import path, include


from . import views

app_name = 'users_app'

urlpatterns = [
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]
