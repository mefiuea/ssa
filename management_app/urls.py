from django.urls import path

from . import views

app_name = 'management_app'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/<int:user_id>', views.profile_edit_view, name='profile_edit_view'),
    path('add-event/', views.event_add_view, name='add_event_view'),
    path('events/', views.events_view, name='events_view'),
]
