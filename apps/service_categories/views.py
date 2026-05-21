from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ServiceCategoryForm
from .models import ServiceCategory


class ServiceCategoryListView(ListView):
	model = ServiceCategory
	template_name = 'service_categories/list_service_categories.html'
	context_object_name = 'service_categories'

	def get_queryset(self):
		queryset = super().get_queryset()
		query = self.request.GET.get('q')

		if query:
			queryset = queryset.filter(
				Q(name__icontains=query)
				| Q(description__icontains=query)
			)

		active = self.request.GET.get('active')
		if active == '1':
			queryset = queryset.filter(is_active=True)
		elif active == '0':
			queryset = queryset.filter(is_active=False)

		return queryset


class ServiceCategoryCreateView(CreateView):
	model = ServiceCategory
	form_class = ServiceCategoryForm
	template_name = 'service_categories/add_service_category.html'
	success_url = reverse_lazy('service_categories:list')


class ServiceCategoryUpdateView(UpdateView):
	model = ServiceCategory
	form_class = ServiceCategoryForm
	template_name = 'service_categories/add_service_category.html'
	success_url = reverse_lazy('service_categories:list')


class ServiceCategoryDeleteView(DeleteView):
	model = ServiceCategory
	template_name = 'service_categories/delete_service_category.html'
	success_url = reverse_lazy('service_categories:list')

# Create your views here.
