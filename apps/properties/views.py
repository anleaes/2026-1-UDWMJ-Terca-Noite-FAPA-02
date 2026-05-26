from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import employee_required

from .forms import PropertyForm
from .models import Property
from rooms.models import Room
from reservations.models import Reservation


def list_properties(request):
    template_name = 'properties/list_properties.html'
    properties = [property for property in list(Property.objects.order_by('name')) if getattr(property, 'is_active', True)]
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
    properties = [property for property in list(Property.objects.filter(name__icontains=query).order_by('name')) if getattr(property, 'is_active', True)]
    context = {'properties': properties, 'query': query}
    return render(request, 'properties/list_properties.html', context)


def detail_property(request, id_property):
    template_name = 'properties/detail_property.html'
    property = get_object_or_404(Property, id=id_property)

    active_reservations = Reservation.objects.select_related('guest').filter(
        status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],
    ).order_by('-created_at')

    rooms = [
        room
        for room in list(
            Room.objects.filter(property=property)
            .select_related('room_type')
            .prefetch_related('amenities', Prefetch('reservations', queryset=active_reservations, to_attr='active_reservations'))
            .order_by('number')
        )
        if getattr(room, 'is_active', True)
    ]
    for room in rooms:
        selected_reservation = room.active_reservations[0] if getattr(room, 'active_reservations', []) else None
        room.selected_reservation = selected_reservation

        if selected_reservation:
            room.display_status_label = 'Selecionado'
            room.display_status_class = 'badge--info'
            room.display_action_label = 'Quarto escolhido'
        elif room.status == 'AVAILABLE':
            room.display_status_label = 'Disponível'
            room.display_status_class = 'badge--success'
            room.display_action_label = 'Reservar agora'
        elif room.status == 'MAINTENANCE':
            room.display_status_label = 'Manutenção'
            room.display_status_class = 'badge--danger'
            room.display_action_label = 'Indisponível'
        else:
            room.display_status_label = 'Não disponível'
            room.display_status_class = 'badge--danger'
            room.display_action_label = 'Indisponível'

    room_count = len(rooms)
    available_count = sum(1 for room in rooms if getattr(room, 'display_status_label', '') == 'Disponível')
    context = {
        'property': property,
        'rooms': rooms,
        'room_count': room_count,
        'available_count': available_count,
    }
    return render(request, template_name, context)
