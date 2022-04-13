from django.urls import path

from . import views

app_name = 'management_app'

urlpatterns = [
    path('add-event/', views.event_add_view, name='add_event_view'),
]
