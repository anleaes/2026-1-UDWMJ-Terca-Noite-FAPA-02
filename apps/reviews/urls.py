from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'reviews'

router = routers.SimpleRouter()
router.register('', views.ReviewViewSet, basename='api-reviews')

urlpatterns = [
    path('listar/', views.list_reviews, name='list_reviews'),
    path('adicionar/', views.add_review, name='add_review'),
    path('editar/<int:id_review>/', views.edit_review, name='edit_review'),
    path('excluir/<int:id_review>/', views.delete_review, name='delete_review'),
    path('buscar/', views.search_reviews, name='search_reviews'),
    path('', include(router.urls)),
]
