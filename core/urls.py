from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('features/', views.features, name='features'),
    path('inventory/', views.inventory_view, name='inventory'),  # Corrected view name
]
