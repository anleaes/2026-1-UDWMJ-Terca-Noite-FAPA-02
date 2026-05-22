from django.urls import path

from . import views

app_name = 'amenities'

urlpatterns = [
    path('listar/', views.list_amenities, name='list_amenities'),
    path('adicionar/', views.add_amenity, name='add_amenity'),
    path('editar/<int:id_amenity>/', views.edit_amenity, name='edit_amenity'),
    path('excluir/<int:id_amenity>/', views.delete_amenity, name='delete_amenity'),
    path('buscar/', views.search_amenities, name='search_amenities'),
]
