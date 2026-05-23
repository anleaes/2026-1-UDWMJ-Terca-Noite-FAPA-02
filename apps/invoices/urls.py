from django.urls import path

from . import views

app_name = 'invoices'

urlpatterns = [
    path('listar/', views.InvoiceListView.as_view(), name='list'),
    path('adicionar/', views.InvoiceCreateView.as_view(), name='add'),
    path('editar/<int:pk>/', views.InvoiceUpdateView.as_view(), name='edit'),
    path('excluir/<int:pk>/', views.InvoiceDeleteView.as_view(), name='delete'),
]