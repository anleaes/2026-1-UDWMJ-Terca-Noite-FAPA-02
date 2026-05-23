from django.db import models

from reservations.models import Reservation


class Invoice(models.Model):
	reservation = models.OneToOneField(
		Reservation,
		on_delete=models.CASCADE,
		related_name='invoice',
		verbose_name='Reserva',
	)
	number = models.CharField('Número', max_length=30, unique=True)
	issue_date = models.DateField('Data de emissão', auto_now_add=True)
	amount = models.FloatField('Valor')
	document_pdf = models.FileField('PDF', upload_to='invoices/', blank=True, null=True)

	class Meta:
		verbose_name = 'Fatura'
		verbose_name_plural = 'Faturas'
		ordering = ['-issue_date']

	def __str__(self):
		return f'Fatura {self.number}'
