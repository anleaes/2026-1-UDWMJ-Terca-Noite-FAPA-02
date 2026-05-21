from django import forms
from .models import Guest


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ('user', 'loyalty_points')
