from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import filters, viewsets

from accounts.decorators import employee_required
from accounts.permissions import IsEmployeeOrReadOnly

from .forms import AmenityForm
from .models import Amenity
from .serializer import AmenitySerializer


def list_amenities(request):
    template_name = 'amenities/list_amenities.html'
    amenities = Amenity.objects.all()
    context = {'amenities': amenities}
    return render(request, template_name, context)


@employee_required
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


@employee_required
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


@employee_required
def delete_amenity(request, id_amenity):
    amenity = get_object_or_404(Amenity, id=id_amenity)
    amenity.delete()
    return redirect('amenities:list_amenities')


def search_amenities(request):
    query = request.GET.get('query', '')
    amenities = Amenity.objects.filter(name__icontains=query)
    context = {'amenities': amenities, 'query': query}
    return render(request, 'amenities/list_amenities.html', context)


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsEmployeeOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
