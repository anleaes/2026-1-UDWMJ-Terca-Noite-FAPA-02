from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import GuestForm
from .models import Guest


@login_required(login_url='/accounts/login/')
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
            return redirect('guests:list_guests')
    else:
        form = GuestForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
def delete_guest(request, id_guest):
    guest = get_object_or_404(Guest, id=id_guest)
    guest.delete()
    return redirect('guests:list_guests')


@login_required(login_url='/accounts/login/')
def search_guests(request):
    template_name = 'guests/list_guests.html'
    query = request.GET.get('query', '')
    guests = Guest.objects.filter(last_name__icontains=query)
    context = {'guests': guests, 'query': query}
    return render(request, template_name, context)
