from django.db import models

from service_categories.models import ServiceCategory


class Service(models.Model):
	category = models.ForeignKey(
		ServiceCategory,
		on_delete=models.PROTECT,
		related_name='services',
		verbose_name='Categoria',
	)
	name = models.CharField('Nome', max_length=100)
	description = models.TextField('Descrição')
	price = models.FloatField('Preço')
	is_active = models.BooleanField('Ativo', default=True)
	photo = models.ImageField('Foto', upload_to='services/', blank=True, null=True)

	class Meta:
		verbose_name = 'Serviço'
		verbose_name_plural = 'Serviços'
		ordering = ['name']

	def __str__(self):
		return self.name
