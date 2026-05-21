from django.db import models


class ServiceCategory(models.Model):
	name = models.CharField('Nome', max_length=50)
	description = models.TextField('Descrição')
	icon = models.ImageField('Ícone', upload_to='service_categories/', blank=True, null=True)
	is_active = models.BooleanField('Ativa', default=True)

	class Meta:
		verbose_name = 'Categoria de Serviço'
		verbose_name_plural = 'Categorias de Serviço'
		ordering = ['name']

	def __str__(self):
		return self.name
