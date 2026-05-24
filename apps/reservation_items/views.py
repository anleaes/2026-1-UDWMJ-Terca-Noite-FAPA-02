from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import employee_required

from .forms import ReservationItemForm
from .models import ReservationItem


@employee_required
def list_reservation_items(request):
    template_name = 'reservation_items/list_reservation_items.html'
    items = ReservationItem.objects.select_related('reservation', 'service').all()
    context = {'items': items}
    return render(request, template_name, context)


@employee_required
def add_reservation_item(request):
    template_name = 'reservation_items/add_reservation_item.html'
    context = {}
    if request.method == 'POST':
        form = ReservationItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_items:list_reservation_items')
    else:
        form = ReservationItemForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_reservation_item(request, id_item):
    template_name = 'reservation_items/add_reservation_item.html'
    item = get_object_or_404(ReservationItem, id=id_item)
    if request.method == 'POST':
        form = ReservationItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('reservation_items:list_reservation_items')
    else:
        form = ReservationItemForm(instance=item)
    return render(request, template_name, {'form': form})


@employee_required
def delete_reservation_item(request, id_item):
    item = get_object_or_404(ReservationItem, id=id_item)
    item.delete()
    return redirect('reservation_items:list_reservation_items')


@employee_required
def search_reservation_items(request):
    template_name = 'reservation_items/list_reservation_items.html'
    query = request.GET.get('query', '')
    items = ReservationItem.objects.select_related('reservation', 'service').filter(
        service__name__icontains=query
    )
    context = {'items': items, 'query': query}
    return render(request, template_name, context)
