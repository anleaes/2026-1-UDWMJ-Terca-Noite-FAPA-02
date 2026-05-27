from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'amenities'

router = routers.SimpleRouter()
router.register('', views.AmenityViewSet, basename='api-amenities')

urlpatterns = [
    path('listar/', views.list_amenities, name='list_amenities'),
    path('adicionar/', views.add_amenity, name='add_amenity'),
    path('editar/<int:id_amenity>/', views.edit_amenity, name='edit_amenity'),
    path('excluir/<int:id_amenity>/', views.delete_amenity, name='delete_amenity'),
    path('buscar/', views.search_amenities, name='search_amenities'),
    path('', include(router.urls)),
]
