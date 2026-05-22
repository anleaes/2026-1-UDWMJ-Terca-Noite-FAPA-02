from django.db import models


class Amenity(models.Model):
    name = models.CharField('Nome', max_length=50)
    description = models.TextField('Descrição')
    icon = models.ImageField('Ícone', upload_to='amenities/', blank=True, null=True)
    is_premium = models.BooleanField('Premium', default=False)

    class Meta:
        verbose_name = 'Comodidade'
        verbose_name_plural = 'Comodidades'
        ordering = ['name']

    def __str__(self):
        return self.name
