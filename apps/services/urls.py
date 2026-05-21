from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('listar/', views.ServiceListView.as_view(), name='list'),
    path('adicionar/', views.ServiceCreateView.as_view(), name='add'),
    path('editar/<int:pk>/', views.ServiceUpdateView.as_view(), name='edit'),
    path('excluir/<int:pk>/', views.ServiceDeleteView.as_view(), name='delete'),
]