from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # REST API endpoints
    path('api/', include('leads.api_urls')),

    # Main CRM website
    path('', include('leads.urls')),
]