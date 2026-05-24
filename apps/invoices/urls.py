from django.urls import path

from . import views

app_name = 'invoices'

urlpatterns = [
    path('listar/', views.list_invoices, name='list_invoices'),
    path('adicionar/', views.add_invoice, name='add_invoice'),
    path('editar/<int:id_invoice>/', views.edit_invoice, name='edit_invoice'),
    path('excluir/<int:id_invoice>/', views.delete_invoice, name='delete_invoice'),
    path('buscar/', views.search_invoices, name='search_invoices'),
]
