from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import ReservationForm
from .models import Reservation


@login_required(login_url='/accounts/login/')
def list_reservations(request):
    template_name = 'reservations/list_reservations.html'
    reservations = Reservation.objects.select_related('guest', 'employee', 'room').all()
    context = {'reservations': reservations}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def delete_reservation(request, id_reservation):
    reservation = get_object_or_404(Reservation, id=id_reservation)
    reservation.delete()
    return redirect('reservations:list_reservations')


@login_required(login_url='/accounts/login/')
def search_reservations(request):
    template_name = 'reservations/list_reservations.html'
    query = request.GET.get('query', '')
    reservations = Reservation.objects.select_related('guest', 'employee', 'room').filter(
        guest__last_name__icontains=query
    )
    context = {'reservations': reservations, 'query': query}
    return render(request, template_name, context)
