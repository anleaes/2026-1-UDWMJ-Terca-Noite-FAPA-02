from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'guests'

router = routers.SimpleRouter()
router.register('', views.GuestViewSet, basename='api-guests')

urlpatterns = [
    path('listar/', views.list_guests, name='list_guests'),
    path('adicionar/', views.add_guest, name='add_guest'),
    path('editar/<int:id_guest>/', views.edit_guest, name='edit_guest'),
    path('excluir/<int:id_guest>/', views.delete_guest, name='delete_guest'),
    path('buscar/', views.search_guests, name='search_guests'),
    path('', include(router.urls)),
]
