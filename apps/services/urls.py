from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('listar/', views.list_services, name='list_services'),
    path('adicionar/', views.add_service, name='add_service'),
    path('editar/<int:id_service>/', views.edit_service, name='edit_service'),
    path('excluir/<int:id_service>/', views.delete_service, name='delete_service'),
    path('buscar/', views.search_services, name='search_services'),
]
