from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import AmenityForm
from .models import Amenity


def list_amenities(request):
    template_name = 'amenities/list_amenities.html'
    amenities = Amenity.objects.all()
    context = {'amenities': amenities}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_amenity(request):
    template_name = 'amenities/add_amenity.html'
    context = {}
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('amenities:list_amenities')
    else:
        form = AmenityForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def edit_amenity(request, id_amenity):
    template_name = 'amenities/add_amenity.html'
    amenity = get_object_or_404(Amenity, id=id_amenity)
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenities:list_amenities')
    else:
        form = AmenityForm(instance=amenity)
    return render(request, template_name, {'form': form})


@login_required(login_url='/accounts/login/')
def delete_amenity(request, id_amenity):
    amenity = get_object_or_404(Amenity, id=id_amenity)
    amenity.delete()
    return redirect('amenities:list_amenities')


def search_amenities(request):
    query = request.GET.get('query', '')
    amenities = Amenity.objects.filter(name__icontains=query)
    context = {'amenities': amenities, 'query': query}
    return render(request, 'amenities/list_amenities.html', context)
