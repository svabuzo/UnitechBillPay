from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('scan/', views.scan_reading_page, name='scan_reading'),
    path('api/upload-reading/', views.api_upload_reading, name='api_upload_reading'),
]