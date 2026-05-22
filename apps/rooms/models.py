from django.db import models

from properties.models import Property
from room_types.models import RoomType
from amenities.models import Amenity


class Room(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponível'),
        ('OCCUPIED', 'Ocupado'),
        ('MAINTENANCE', 'Manutenção'),
    ]
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='rooms', verbose_name='Propriedade')
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='rooms', verbose_name='Tipo')
    amenities = models.ManyToManyField(Amenity, related_name='rooms', blank=True, verbose_name='Comodidades')
    number = models.CharField('Número', max_length=10)
    floor = models.IntegerField('Andar')
    description = models.TextField('Descrição')
    daily_rate = models.FloatField('Diária')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    is_active = models.BooleanField('Ativo', default=True)
    photo = models.ImageField('Foto', upload_to='rooms/', blank=True, null=True)

    class Meta:
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'
        ordering = ['property', 'number']

    def __str__(self):
        return f'{self.property.name} - Quarto {self.number}'
