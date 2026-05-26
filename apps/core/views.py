from django.db import DatabaseError
from django.shortcuts import render

from properties.models import Property


def home(request):
    template_name = 'core/home.html'
    try:
        featured_properties = [property for property in list(Property.objects.order_by('-rating')[:6]) if getattr(property, 'is_active', True)]
    except DatabaseError:
        featured_properties = []
    context = {'featured_properties': featured_properties}
    return render(request, template_name, context)
