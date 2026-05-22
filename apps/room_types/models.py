from django.db import models


class RoomType(models.Model):
    name = models.CharField('Nome', max_length=50)
    description = models.TextField('Descrição')
    base_price = models.FloatField('Preço base')
    max_occupancy = models.IntegerField('Ocupação máxima')

    class Meta:
        verbose_name = 'Tipo de Quarto'
        verbose_name_plural = 'Tipos de Quarto'
        ordering = ['name']

    def __str__(self):
        return self.name
