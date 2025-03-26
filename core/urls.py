from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('features/', views.features, name='features'),
    path('inventory/', views.inventory_view, name='inventory'), 
    path('stock-analysis/', views.stock_analysis_view, name='stock_analysis'),
    path('alternate-medicine/', views.alternate_medicine_view, name='alternate_medicine'),
    path('upload-prescription/', views.upload_prescription_view, name='upload_prescription'),
    path('upload-medicine-image/', views.upload_medicine_image_view, name='upload_medicine_image'),
    path('side-effects/', views.side_effects_view, name='side_effects'),
    path('dashboard/', views.dashboard_view, name='dashboard'),# Corrected view name
]
