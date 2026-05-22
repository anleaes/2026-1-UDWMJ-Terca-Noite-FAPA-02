from django import forms

from .models import Amenity


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        exclude = ()
