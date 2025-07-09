from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime
from decimal import Decimal

# Create your models here.


class Republica(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    #Novo campo para ligar uma pessoa a um usuário no Django:
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pessoa_profile')

    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    telefone = models.CharField(max_length=15)
    republica = models.ForeignKey('Republica', related_name='pessoas', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    republica = models.ForeignKey('Republica', related_name='contas', on_delete=models.CASCADE)
    nome_conta = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    paga = models.BooleanField(default=False)

    def __str__(self):
        status = "Paga" if self.paga else "Pendente"
        return f"{self.nome_conta} - R$ {self.valor} - ({status})"

    # As contas serão ordenados por "data_vencimento" em ordem decrescente.
    class Meta:
        ordering = ['-data_vencimento']


class Pagamento(models.Model):
    pessoa = models.ForeignKey('Pessoa', related_name='pagamentos', on_delete=models.CASCADE)
    conta = models.ForeignKey('Conta', related_name='pagamentos', on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pessoa.nome} pagou R$ {self.valor_pago} - {self.conta.nome_conta} em {self.data_pagamento}"

    def save(self, *args, **kwargs):

        # Ao salvar o pagamento, marca a conta como paga
        super().save(*args, **kwargs)
        self.conta.paga = True
        self.conta.save()

    class Meta:
        # Os pagamentos serão ordenados por "data_pagamento" em ordem decrescente.
        ordering = ['-data_pagamento']

        # Impede que a mesma pessoa pague a mesma conta mais de uma vez
        unique_together = ['pessoa' , 'conta']
