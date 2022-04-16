from django.urls import path

from . import views

app_name = 'management_app'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/<int:user_id>/', views.profile_edit_view, name='profile_edit_view'),
    path('add-event/', views.event_add_view, name='add_event_view'),
    path('events/', views.events_view, name='events_view'),
    path('event-detailed-view/<int:event_id>/', views.event_detailed_view, name='event_detailed_view'),
    path('event-edit-view/<int:event_id>/', views.event_edit_view, name='event_edit_view'),
    path('event-delete-view/<int:event_id>/', views.event_delete_view, name='event_delete_view'),
    path('persons-view/', views.persons_view, name='persons_view'),
]
