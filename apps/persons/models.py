from django.db import models


class Person(models.Model):
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=100)
    address = models.CharField('Endereço', max_length=200)
    phone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail')

    class Meta:
        abstract = True
        ordering = ['first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
