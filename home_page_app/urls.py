from django.urls import path

from . import views

app_name = 'home_page_app'

urlpatterns = [
    path('', views.home_page_view, name='home_view'),
    path('thread/<int:post_id>', views.thread_view, name='thread_view'),
]
