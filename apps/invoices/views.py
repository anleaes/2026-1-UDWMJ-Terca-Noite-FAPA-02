from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import employee_required

from .forms import InvoiceForm
from .models import Invoice


@employee_required
def list_invoices(request):
    template_name = 'invoices/list_invoices.html'
    invoices = Invoice.objects.select_related('reservation', 'reservation__guest', 'reservation__room').all()
    context = {'invoices': invoices}
    return render(request, template_name, context)


@employee_required
def add_invoice(request):
    template_name = 'invoices/add_invoice.html'
    context = {}
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('invoices:list_invoices')
    else:
        form = InvoiceForm()
    context['form'] = form
    return render(request, template_name, context)


@employee_required
def edit_invoice(request, id_invoice):
    template_name = 'invoices/add_invoice.html'
    invoice = get_object_or_404(Invoice, id=id_invoice)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoices:list_invoices')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, template_name, {'form': form})


@employee_required
def delete_invoice(request, id_invoice):
    invoice = get_object_or_404(Invoice, id=id_invoice)
    invoice.delete()
    return redirect('invoices:list_invoices')


@employee_required
def search_invoices(request):
    template_name = 'invoices/list_invoices.html'
    query = request.GET.get('query', '')
    invoices = Invoice.objects.select_related('reservation', 'reservation__guest', 'reservation__room').filter(
        Q(number__icontains=query)
        | Q(reservation__guest__first_name__icontains=query)
        | Q(reservation__guest__last_name__icontains=query)
        | Q(reservation__room__number__icontains=query)
    )
    context = {'invoices': invoices, 'query': query}
    return render(request, template_name, context)
