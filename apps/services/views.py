from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServiceForm
from .models import Service


def list_services(request):
    template_name = 'services/list_services.html'
    services = Service.objects.select_related('category').filter(is_active=True)
    context = {'services': services}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_service(request):
    template_name = 'services/add_service.html'
    context = {}
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('services:list_services')
    else:
        form = ServiceForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def edit_service(request, id_service):
    template_name = 'services/add_service.html'
    service = get_object_or_404(Service, id=id_service)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services:list_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, template_name, {'form': form})


@login_required(login_url='/accounts/login/')
def delete_service(request, id_service):
    service = get_object_or_404(Service, id=id_service)
    service.delete()
    return redirect('services:list_services')


def search_services(request):
    template_name = 'services/list_services.html'
    query = request.GET.get('query', '')
    services = Service.objects.select_related('category').filter(
        Q(name__icontains=query)
        | Q(description__icontains=query)
        | Q(category__name__icontains=query)
    )
    context = {'services': services, 'query': query}
    return render(request, template_name, context)
