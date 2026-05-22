from django.urls import path

from . import views

app_name = 'room_types'

urlpatterns = [
    path('listar/', views.list_room_types, name='list_room_types'),
    path('adicionar/', views.add_room_type, name='add_room_type'),
    path('editar/<int:id_room_type>/', views.edit_room_type, name='edit_room_type'),
    path('excluir/<int:id_room_type>/', views.delete_room_type, name='delete_room_type'),
    path('buscar/', views.search_room_types, name='search_room_types'),
]
