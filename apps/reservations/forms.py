from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ('created_at',)


class ReservationBookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('check_in', 'check_out', 'guests_count', 'payment_method', 'notes')
