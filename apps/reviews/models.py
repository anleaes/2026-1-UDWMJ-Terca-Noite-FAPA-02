from django.db import models

from reservations.models import Reservation


class Review(models.Model):
	reservation = models.OneToOneField(
		Reservation,
		on_delete=models.CASCADE,
		related_name='review',
		verbose_name='Reserva',
	)
	rating = models.IntegerField('Nota (1-5)')
	comment = models.TextField('Comentário')
	created_at = models.DateTimeField('Criada em', auto_now_add=True)
	photo = models.ImageField('Foto', upload_to='reviews/', blank=True, null=True)
	is_approved = models.BooleanField('Aprovada', default=False)

	class Meta:
		verbose_name = 'Avaliação'
		verbose_name_plural = 'Avaliações'
		ordering = ['-created_at']

	def __str__(self):
		return f'Avaliação {self.rating}/5 - Reserva #{self.reservation.id}'
