from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from .models import Employee


@login_required(login_url='/accounts/login/')
def list_employees(request):
    template_name = 'employees/list_employees.html'
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def add_employee(request):
    template_name = 'employees/add_employee.html'
    context = {}
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employees:list_employees')
    else:
        form = EmployeeForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def edit_employee(request, id_employee):
    template_name = 'employees/add_employee.html'
    employee = get_object_or_404(Employee, id=id_employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:list_employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, template_name, {'form': form})


@login_required(login_url='/accounts/login/')
def delete_employee(request, id_employee):
    employee = get_object_or_404(Employee, id=id_employee)
    employee.delete()
    return redirect('employees:list_employees')


@login_required(login_url='/accounts/login/')
def search_employees(request):
    template_name = 'employees/list_employees.html'
    query = request.GET.get('query', '')
    employees = Employee.objects.filter(last_name__icontains=query)
    context = {'employees': employees, 'query': query}
    return render(request, template_name, context)
