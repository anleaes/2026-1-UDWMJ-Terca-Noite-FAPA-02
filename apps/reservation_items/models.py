from django.db import models

from reservations.models import Reservation
from services.models import Service


class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='items', verbose_name='Reserva')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='reservation_items', verbose_name='Serviço')
    quantity = models.IntegerField('Quantidade', default=1)
    unit_price = models.FloatField('Preço unitário')
    subtotal = models.FloatField('Subtotal')
    service_date = models.DateField('Data do serviço')

    class Meta:
        verbose_name = 'Item de Reserva'
        verbose_name_plural = 'Itens de Reserva'
        ordering = ['service_date']

    def __str__(self):
        return f'{self.service.name} x{self.quantity}'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
