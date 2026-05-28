from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'reservation_items'

router = routers.SimpleRouter()
router.register('', views.ReservationItemViewSet, basename='api-reservation-items')

urlpatterns = [
    path('listar/', views.list_reservation_items, name='list_reservation_items'),
    path('adicionar/', views.add_reservation_item, name='add_reservation_item'),
    path('editar/<int:id_item>/', views.edit_reservation_item, name='edit_reservation_item'),
    path('excluir/<int:id_item>/', views.delete_reservation_item, name='delete_reservation_item'),
    path('buscar/', views.search_reservation_items, name='search_reservation_items'),
    path('', include(router.urls)),
]
