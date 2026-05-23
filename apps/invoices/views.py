from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import InvoiceForm
from .models import Invoice


class InvoiceListView(ListView):
	model = Invoice
	template_name = 'invoices/list_invoices.html'
	context_object_name = 'invoices'

	def get_queryset(self):
		queryset = super().get_queryset().select_related('reservation', 'reservation__guest', 'reservation__room')
		query = self.request.GET.get('q')

		if query:
			queryset = queryset.filter(
				Q(number__icontains=query)
				| Q(reservation__id__icontains=query)
				| Q(reservation__guest__first_name__icontains=query)
				| Q(reservation__guest__last_name__icontains=query)
				| Q(reservation__room__number__icontains=query)
			)

		reservation_id = self.request.GET.get('reservation')
		if reservation_id:
			queryset = queryset.filter(reservation__id=reservation_id)

		return queryset


class InvoiceCreateView(CreateView):
	model = Invoice
	form_class = InvoiceForm
	template_name = 'invoices/add_invoice.html'
	success_url = reverse_lazy('invoices:list')


class InvoiceUpdateView(UpdateView):
	model = Invoice
	form_class = InvoiceForm
	template_name = 'invoices/add_invoice.html'
	success_url = reverse_lazy('invoices:list')


class InvoiceDeleteView(DeleteView):
	model = Invoice
	template_name = 'invoices/delete_invoice.html'
	success_url = reverse_lazy('invoices:list')

# Create your views here.
