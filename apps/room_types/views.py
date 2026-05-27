from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import filters, viewsets

from accounts.decorators import employee_required
from accounts.permissions import IsEmployeeOrReadOnly

from .forms import RoomTypeForm
from .models import RoomType
from .serializer import RoomTypeSerializer


def list_room_types(request):
    template_name = 'room_types/list_room_types.html'
    room_types = RoomType.objects.all()
    context = {'room_types': room_types}
    return render(request, template_name, context)


@employee_required
def add_room_type(request):
    template_name = 'room_types/add_room_type.html'
    context = {}
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_types:list_room_types')
    else:
        form = RoomTypeForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_room_type(request, id_room_type):
    template_name = 'room_types/add_room_type.html'
    room_type = get_object_or_404(RoomType, id=id_room_type)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            return redirect('room_types:list_room_types')
    else:
        form = RoomTypeForm(instance=room_type)
    return render(request, template_name, {'form': form})


@employee_required
def delete_room_type(request, id_room_type):
    room_type = get_object_or_404(RoomType, id=id_room_type)
    room_type.delete()
    return redirect('room_types:list_room_types')


def search_room_types(request):
    query = request.GET.get('query', '')
    room_types = RoomType.objects.filter(name__icontains=query)
    context = {'room_types': room_types, 'query': query}
    return render(request, 'room_types/list_room_types.html', context)


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsEmployeeOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'base_price']
