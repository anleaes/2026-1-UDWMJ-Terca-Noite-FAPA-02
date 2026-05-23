from django import forms

from .models import ReservationItem


class ReservationItemForm(forms.ModelForm):
    class Meta:
        model = ReservationItem
        exclude = ('subtotal',)
