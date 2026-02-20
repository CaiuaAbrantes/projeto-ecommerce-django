from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validacpf import valida_cpf
import re

class Perfil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complmento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user}'
    
    def clean(self):
        erro_massages = {}
        if not valida_cpf(self.cpf):
            erro_massages['cpf'] = 'Cpf invalido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) <8:
            erro_massages['cep'] = 'Cep invalido, digite os 8 digitos do cep'

        if erro_massages:
            raise ValidationError(erro_massages)

    class Meta():
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'