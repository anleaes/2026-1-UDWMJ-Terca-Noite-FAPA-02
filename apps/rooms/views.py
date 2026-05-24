from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import employee_required

from .forms import RoomForm
from .models import Room


def list_rooms(request):
    template_name = 'rooms/list_rooms.html'
    rooms = Room.objects.filter(is_active=True)
    context = {'rooms': rooms}
    return render(request, template_name, context)


@employee_required
def add_room(request):
    template_name = 'rooms/add_room.html'
    context = {}
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rooms:list_rooms')
    else:
        form = RoomForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_room(request, id_room):
    template_name = 'rooms/add_room.html'
    room = get_object_or_404(Room, id=id_room)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms:list_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, template_name, {'form': form})


@employee_required
def delete_room(request, id_room):
    room = get_object_or_404(Room, id=id_room)
    room.delete()
    return redirect('rooms:list_rooms')


def search_rooms(request):
    query = request.GET.get('query', '')
    rooms = Room.objects.filter(number__icontains=query, is_active=True)
    context = {'rooms': rooms, 'query': query}
    return render(request, 'rooms/list_rooms.html', context)
