from django import forms

from reservations.models import Reservation

from .models import ReservationItem


class ReservationItemForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        reservations = Reservation.objects.select_related('guest', 'room__property')
        if user and user.is_superuser:
            queryset = reservations.filter(status__in=['PENDING', 'CONFIRMED'])
        else:
            guest_profile = getattr(user, 'guest_profile', None)
            queryset = (
                reservations.filter(guest=guest_profile, status__in=['PENDING', 'CONFIRMED'])
                if guest_profile
                else reservations.none()
            )

        if self.instance and self.instance.pk and self.instance.reservation_id:
            queryset = queryset | Reservation.objects.filter(pk=self.instance.reservation_id)

        self.fields['reservation'].queryset = queryset.distinct().order_by('-created_at')

    class Meta:
        model = ReservationItem
        exclude = ('subtotal',)
