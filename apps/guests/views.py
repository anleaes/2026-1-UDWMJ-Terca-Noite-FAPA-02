from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.decorators import employee_required
from accounts.permissions import IsEmployee

from .forms import GuestForm
from .models import Guest
from .serializer import GuestSerializer


@employee_required
def list_guests(request):
    template_name = 'guests/list_guests.html'
    guests = Guest.objects.all()
    context = {'guests': guests}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_guest(request):
    template_name = 'guests/add_guest.html'
    context = {}
    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save(commit=False)
            if not request.user.is_staff:
                guest.user = request.user
            guest.save()
            if hasattr(request.user, 'employee_profile'):
                return redirect('guests:list_guests')
            return redirect('core:home')
    else:
        form = GuestForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_guest(request, id_guest):
    template_name = 'guests/add_guest.html'
    guest = get_object_or_404(Guest, id=id_guest)
    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('guests:list_guests')
    else:
        form = GuestForm(instance=guest)
    return render(request, template_name, {'form': form})


@employee_required
def delete_guest(request, id_guest):
    guest = get_object_or_404(Guest, id=id_guest)
    guest.delete()
    return redirect('guests:list_guests')


@employee_required
def search_guests(request):
    template_name = 'guests/list_guests.html'
    query = request.GET.get('query', '')
    guests = Guest.objects.filter(last_name__icontains=query)
    context = {'guests': guests, 'query': query}
    return render(request, template_name, context)


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'document', 'email']
    ordering_fields = ['first_name', 'last_name', 'loyalty_points']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsEmployee()]
