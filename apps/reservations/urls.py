from django.urls import path

from . import views

app_name = 'reservations'

urlpatterns = [
    path('listar/', views.list_reservations, name='list_reservations'),
    path('adicionar/', views.add_reservation, name='add_reservation'),
    path('editar/<int:id_reservation>/', views.edit_reservation, name='edit_reservation'),
    path('excluir/<int:id_reservation>/', views.delete_reservation, name='delete_reservation'),
    path('buscar/', views.search_reservations, name='search_reservations'),
]
