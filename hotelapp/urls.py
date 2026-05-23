"""
URL configuration for hotelapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('service_categories/', include('service_categories.urls', namespace='service_categories')),
    path('services/', include('services.urls', namespace='services')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('guests/', include('guests.urls', namespace='guests')),
    path('employees/', include('employees.urls', namespace='employees')),
    path('properties/', include('properties.urls', namespace='properties')),
    path('room_types/', include('room_types.urls', namespace='room_types')),
    path('amenities/', include('amenities.urls', namespace='amenities')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
    path('reservation_items/', include('reservation_items.urls', namespace='reservation_items')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
