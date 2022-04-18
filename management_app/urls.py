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
    path('add-offer/', views.offer_add_view, name='add_offer_view'),
    path('market/', views.market_view, name='market_view'),
    path('offer-detailed-view/<int:offer_id>/', views.offer_detailed_view, name='offer_detailed_view'),
    path('offer-edit-view/<int:offer_id>/', views.offer_edit_view, name='offer_edit_view'),
    path('offer-delete-view/<int:offer_id>/', views.offer_delete_view, name='offer_delete_view'),
]
