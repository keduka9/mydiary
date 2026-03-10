from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/new/', views.entry_new, name='entry_new'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),

    # REST API用URL
    path('api/entries/', views.EntryListAPI.as_view(), name='api_entry_list'),
    path('api/entries/<int:pk>/', views.EntryDetailAPI.as_view(), name='api_entry_detail'),
]