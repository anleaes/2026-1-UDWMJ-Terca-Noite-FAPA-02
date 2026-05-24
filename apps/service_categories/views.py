from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import employee_required

from .forms import ServiceCategoryForm
from .models import ServiceCategory


def list_service_categories(request):
    template_name = 'service_categories/list_service_categories.html'
    categories = ServiceCategory.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, template_name, context)


@employee_required
def add_service_category(request):
    template_name = 'service_categories/add_service_category.html'
    context = {}
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_categories:list_service_categories')
    else:
        form = ServiceCategoryForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_service_category(request, id_category):
    template_name = 'service_categories/add_service_category.html'
    category = get_object_or_404(ServiceCategory, id=id_category)
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('service_categories:list_service_categories')
    else:
        form = ServiceCategoryForm(instance=category)
    return render(request, template_name, {'form': form})


@employee_required
def delete_service_category(request, id_category):
    category = get_object_or_404(ServiceCategory, id=id_category)
    category.delete()
    return redirect('service_categories:list_service_categories')


def search_service_categories(request):
    template_name = 'service_categories/list_service_categories.html'
    query = request.GET.get('query', '')
    categories = ServiceCategory.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    context = {'categories': categories, 'query': query}
    return render(request, template_name, context)
