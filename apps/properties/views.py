from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import employee_required

from .forms import PropertyForm
from .models import Property


def list_properties(request):
    template_name = 'properties/list_properties.html'
    properties = Property.objects.filter(is_active=True)
    context = {'properties': properties}
    return render(request, template_name, context)


@employee_required
def add_property(request):
    template_name = 'properties/add_property.html'
    context = {}
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('properties:list_properties')
    else:
        form = PropertyForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_property(request, id_property):
    template_name = 'properties/add_property.html'
    property = get_object_or_404(Property, id=id_property)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('properties:list_properties')
    else:
        form = PropertyForm(instance=property)
    return render(request, template_name, {'form': form})


@employee_required
def delete_property(request, id_property):
    property = get_object_or_404(Property, id=id_property)
    property.delete()
    return redirect('properties:list_properties')


def search_properties(request):
    query = request.GET.get('query', '')
    properties = Property.objects.filter(name__icontains=query, is_active=True)
    context = {'properties': properties, 'query': query}
    return render(request, 'properties/list_properties.html', context)
