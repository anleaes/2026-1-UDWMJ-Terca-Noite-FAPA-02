from django.db import models
from django.contrib.auth.models import User
from persons.models import Person


class Guest(Person):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest_profile', null=True, blank=True, verbose_name='Usuário')
    birth_date = models.DateField('Data de nascimento')
    document = models.CharField('Documento', max_length=20, unique=True)
    gender = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES)
    loyalty_points = models.IntegerField('Pontos de fidelidade', default=0)
    profile_photo = models.ImageField('Foto', upload_to='guests/', blank=True, null=True)

    class Meta:
        verbose_name = 'Hóspede'
        verbose_name_plural = 'Hóspedes'
        ordering = ['first_name']
