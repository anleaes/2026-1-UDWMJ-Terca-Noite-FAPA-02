from django.db import models
from django.contrib.auth.models import User
from persons.models import Person


class Employee(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True, verbose_name='Usuário')
    salary = models.FloatField('Salário')
    position = models.CharField('Cargo', max_length=50)
    hired_date = models.DateField('Data de contratação')
    is_active = models.BooleanField('Ativo', default=True)
    contract = models.FileField('Contrato', upload_to='contracts/', blank=True, null=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['first_name']
