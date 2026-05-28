import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.decorators import superuser_required
from guests.models import Guest
from invoices.models import Invoice
from rooms.models import Room

from .forms import ReservationBookingForm, ReservationForm
from .models import Reservation
from .serializer import ReservationSerializer


@login_required(login_url='/accounts/login/')
def list_reservations(request):
    template_name = 'reservations/list_reservations.html'
    reservations = Reservation.objects.select_related('guest', 'employee', 'room')
    if request.user.is_superuser:
        reservations = reservations.all()
        can_manage = True
    else:
        reservations = reservations.filter(guest__user=request.user)
        can_manage = False
    context = {'reservations': reservations, 'can_manage_reservations': can_manage}
    return render(request, template_name, context)


@superuser_required
def add_reservation(request):
    template_name = 'reservations/add_reservation.html'
    context = {}
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations:list_reservations')
    else:
        form = ReservationForm()
    context['form'] = form
    return render(request, template_name, context)


@superuser_required
def edit_reservation(request, id_reservation):
    template_name = 'reservations/add_reservation.html'
    reservation = get_object_or_404(Reservation, id=id_reservation)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations:list_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, template_name, {'form': form})


@superuser_required
def delete_reservation(request, id_reservation):
    reservation = get_object_or_404(Reservation, id=id_reservation)
    reservation.delete()
    return redirect('reservations:list_reservations')


@login_required(login_url='/accounts/login/')
def search_reservations(request):
    template_name = 'reservations/list_reservations.html'
    query = request.GET.get('query', '')
    reservations = Reservation.objects.select_related('guest', 'employee', 'room')
    if request.user.is_superuser:
        reservations = reservations.filter(guest__last_name__icontains=query)
        can_manage = True
    else:
        reservations = reservations.filter(guest__user=request.user, guest__last_name__icontains=query)
        can_manage = False
    context = {'reservations': reservations, 'query': query, 'can_manage_reservations': can_manage}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def book_room(request, id_room):
    template_name = 'reservations/book_room.html'
    room = get_object_or_404(Room, id=id_room)
    try:
        guest = request.user.guest_profile
    except (Guest.DoesNotExist, AttributeError):
        return redirect('guests:add_guest')
    if request.method == 'POST':
        form = ReservationBookingForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.guest = guest
            reservation.room = room
            reservation.total = (reservation.check_out - reservation.check_in).days * room.daily_rate
            reservation.save()
            return redirect('properties:detail_property', id_property=room.property.id)
    else:
        form = ReservationBookingForm()
    context = {'form': form, 'room': room}
    return render(request, template_name, context)


@superuser_required
def confirm_reservation(request, id_reservation):
    reservation = get_object_or_404(Reservation, id=id_reservation)
    reservation.status = 'CONFIRMED'
    reservation.save()
    Invoice.objects.get_or_create(
        reservation=reservation,
        defaults={
            'number': f'INV-{uuid.uuid4().hex[:8].upper()}',
            'amount': reservation.total,
        },
    )
    return redirect('reservations:list_reservations')


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['guest__first_name', 'guest__last_name', 'room__number']
    ordering_fields = ['check_in', 'check_out', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employee_profile'):
            return Reservation.objects.select_related('guest', 'employee', 'room').all()
        if hasattr(user, 'guest_profile'):
            return Reservation.objects.select_related('guest', 'employee', 'room').filter(
                guest=user.guest_profile
            )
        return Reservation.objects.none()

    @action(detail=False, methods=['post'], url_path=r'book/(?P<id_room>\d+)')
    def book_room(self, request, id_room=None):
        room = get_object_or_404(Room, id=id_room)
        try:
            guest = request.user.guest_profile
        except (Guest.DoesNotExist, AttributeError):
            return Response({'detail': 'Cadastro de hospede necessario.'}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        reservation = serializer.save(
            guest=guest,
            room=room,
            total=(check_out - check_in).days * room.daily_rate,
        )
        return Response(self.get_serializer(reservation).data, status=201)

    @action(detail=True, methods=['post'], permission_classes=[IsEmployee])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'CONFIRMED'
        reservation.save()
        Invoice.objects.get_or_create(
            reservation=reservation,
            defaults={
                'number': f'INV-{uuid.uuid4().hex[:8].upper()}',
                'amount': reservation.total,
            },
        )
        return Response(self.get_serializer(reservation).data)
