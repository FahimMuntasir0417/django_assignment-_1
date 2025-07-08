from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.manager_dashboard, name='dashboard'),

    path('events_list/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='event_create'),
    path('events/<int:pk>/update/', views.update_event, name='event_update'),
    path('events/<int:pk>/delete/', views.delete_event, name='event_delete'),

    path('participants/', views.participant_list, name='participant_list'),
    path('participants/<int:pk>/', views.participant_detail, name='participant_detail'),
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
