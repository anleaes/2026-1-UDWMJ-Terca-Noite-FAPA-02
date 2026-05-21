from django.urls import path
from . import views

app_name = 'guests'

urlpatterns = [
    path('listar/', views.list_guests, name='list_guests'),
    path('adicionar/', views.add_guest, name='add_guest'),
    path('editar/<int:id_guest>/', views.edit_guest, name='edit_guest'),
    path('excluir/<int:id_guest>/', views.delete_guest, name='delete_guest'),
    path('buscar/', views.search_guests, name='search_guests'),
]
