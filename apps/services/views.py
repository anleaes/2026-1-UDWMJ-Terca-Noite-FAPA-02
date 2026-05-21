from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ServiceForm
from .models import Service


class ServiceListView(ListView):
	model = Service
	template_name = 'services/list_services.html'
	context_object_name = 'services'

	def get_queryset(self):
		queryset = super().get_queryset()
		query = self.request.GET.get('q')

		if query:
			queryset = queryset.filter(
				Q(name__icontains=query)
				| Q(description__icontains=query)
				| Q(category__name__icontains=query)
			)

		active = self.request.GET.get('active')
		if active == '1':
			queryset = queryset.filter(is_active=True)
		elif active == '0':
			queryset = queryset.filter(is_active=False)

		return queryset


class ServiceCreateView(CreateView):
	model = Service
	form_class = ServiceForm
	template_name = 'services/add_service.html'
	success_url = reverse_lazy('services:list')


class ServiceUpdateView(UpdateView):
	model = Service
	form_class = ServiceForm
	template_name = 'services/add_service.html'
	success_url = reverse_lazy('services:list')


class ServiceDeleteView(DeleteView):
	model = Service
	template_name = 'services/delete_service.html'
	success_url = reverse_lazy('services:list')

# Create your views here.
