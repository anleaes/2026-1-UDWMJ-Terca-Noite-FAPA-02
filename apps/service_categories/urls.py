from django.urls import path

from . import views

app_name = 'service_categories'

urlpatterns = [
    path('listar/', views.ServiceCategoryListView.as_view(), name='list'),
    path('adicionar/', views.ServiceCategoryCreateView.as_view(), name='add'),
    path('editar/<int:pk>/', views.ServiceCategoryUpdateView.as_view(), name='edit'),
    path('excluir/<int:pk>/', views.ServiceCategoryDeleteView.as_view(), name='delete'),
]