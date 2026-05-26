from django.urls import path

from . import views

app_name = 'properties'

urlpatterns = [
    path('listar/', views.list_properties, name='list_properties'),
    path('detalhe/<int:id_property>/', views.detail_property, name='detail_property'),
    path('adicionar/', views.add_property, name='add_property'),
    path('editar/<int:id_property>/', views.edit_property, name='edit_property'),
    path('excluir/<int:id_property>/', views.delete_property, name='delete_property'),
    path('buscar/', views.search_properties, name='search_properties'),
]
