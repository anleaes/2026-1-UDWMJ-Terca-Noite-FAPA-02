from django.db import models

from guests.models import Guest
from employees.models import Employee
from rooms.models import Room


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('CONFIRMED', 'Confirmada'),
        ('CHECKED_IN', 'Check-in'),
        ('CHECKED_OUT', 'Check-out'),
        ('CANCELED', 'Cancelada'),
    ]
    PAYMENT_CHOICES = [
        ('CASH', 'Dinheiro'),
        ('CREDIT', 'Cartão de crédito'),
        ('DEBIT', 'Cartão de débito'),
        ('PIX', 'PIX'),
    ]
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='reservations', verbose_name='Hóspede')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='reservations', verbose_name='Funcionário', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='reservations', verbose_name='Quarto')
    check_in = models.DateField('Check-in')
    check_out = models.DateField('Check-out')
    created_at = models.DateTimeField('Criada em', auto_now_add=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField('Forma de pagamento', max_length=20, choices=PAYMENT_CHOICES)
    total = models.FloatField('Total', default=0.0)
    guests_count = models.IntegerField('Nº de hóspedes', default=1)
    notes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reserva #{self.id} - {self.guest}'
