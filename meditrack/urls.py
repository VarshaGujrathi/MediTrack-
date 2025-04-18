"""
URL configuration for meditrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views  # Include this for app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', include('core.urls')),  
    path('features/', views.features, name='features'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('upload_prescription/', views.upload_prescription, name='upload_prescription'),   path('nearby-medical/', views.nearby_medical_view, name='nearby_medical'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
