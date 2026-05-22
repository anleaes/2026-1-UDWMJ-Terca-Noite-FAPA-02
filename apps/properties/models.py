from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = [
        ('HOTEL', 'Hotel'),
        ('POUSADA', 'Pousada'),
        ('RESORT', 'Resort'),
        ('HOSTEL', 'Hostel'),
    ]
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    address = models.CharField('Endereço', max_length=200)
    property_type = models.CharField('Tipo', max_length=20, choices=PROPERTY_TYPES)
    rating = models.FloatField('Avaliação', default=0.0)
    photo = models.ImageField('Foto', upload_to='properties/', blank=True, null=True)
    is_active = models.BooleanField('Ativa', default=True)
    created_at = models.DateTimeField('Criada em', auto_now_add=True)

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'
        ordering = ['name']

    def __str__(self):
        return self.name
