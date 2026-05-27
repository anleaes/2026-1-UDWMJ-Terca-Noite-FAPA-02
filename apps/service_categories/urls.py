from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'service_categories'

router = routers.SimpleRouter()
router.register('', views.ServiceCategoryViewSet, basename='api-service-categories')

urlpatterns = [
    path('listar/', views.list_service_categories, name='list_service_categories'),
    path('adicionar/', views.add_service_category, name='add_service_category'),
    path('editar/<int:id_category>/', views.edit_service_category, name='edit_service_category'),
    path('excluir/<int:id_category>/', views.delete_service_category, name='delete_service_category'),
    path('buscar/', views.search_service_categories, name='search_service_categories'),
    path('', include(router.urls)),
]
