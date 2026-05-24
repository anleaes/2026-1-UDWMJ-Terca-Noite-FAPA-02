from django.shortcuts import render

from properties.models import Property


def home(request):
    template_name = 'core/home.html'
    featured_properties = Property.objects.filter(is_active=True).order_by('-rating')[:3]
    context = {'featured_properties': featured_properties}
    return render(request, template_name, context)
