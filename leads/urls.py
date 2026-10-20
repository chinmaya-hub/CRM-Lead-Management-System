from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Lead Management
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/<int:lead_id>/edit/', views.edit_lead, name='edit_lead'),
    path('leads/<int:lead_id>/delete/', views.delete_lead, name='delete_lead'),

    # Activity Logs
    path(
        'leads/<int:lead_id>/activities/',
        views.lead_activities,
        name='lead_activities'
    ),

    # Follow-up Management
    path(
        'leads/<int:lead_id>/followups/',
        views.lead_followups,
        name='lead_followups'
    ),

    # Lead-to-Customer Conversion
    path(
        'leads/<int:lead_id>/convert/',
        views.convert_lead,
        name='convert_lead'
    ),
]