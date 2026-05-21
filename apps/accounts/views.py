from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    template_name = 'accounts/login.html'
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'employee_profile'):
                return redirect('reservations:list_reservations')
            return redirect('core:home')
        context['erro'] = 'Usuário ou senha inválidos.'
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect('core:home')


def register_view(request):
    template_name = 'accounts/register.html'
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        context['form'] = form
    else:
        context['form'] = UserCreationForm()
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def profile_view(request):
    template_name = 'accounts/profile.html'
    context = {'user': request.user}
    return render(request, template_name, context)
