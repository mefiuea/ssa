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
    path('add-post/', views.post_add_view, name='add_post_view'),
    path('thread/<int:post_id>', views.thread_view, name='thread_view'),
    path('post-edit-view/<int:post_id>/', views.post_edit_view, name='post_edit_view'),
    path('comment-edit-view/<int:post_id>/<int:comment_id>', views.comment_edit_view, name='comment_edit_view'),
    path('contact', views.contact_view, name='contact_view'),
]
