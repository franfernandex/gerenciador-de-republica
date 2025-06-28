from django.db import models

# Create your models here.


class Republica(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    @property
    def moradores(self):
        return self.pessoas.all()  # related_name='pessoas'

    @property
    def contas(self):
        return self.contas.all()  # related_name='contas'

    def adicionar_morador(self, pessoa):
        pessoa.republica = self
        pessoa.save()

    def remover_morador(self, pessoa):
        if pessoa.republica == self:
            pessoa.delete()

    def adicionar_conta(self, conta):
        conta.republica = self
        conta.save()

    def remover_conta(self, conta):
        if conta.republica == self:
            conta.delete()

    def listar_moradores(self):
        return self.moradores

    def listar_contas(self):
        return self.contas

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    telefone = models.CharField(max_length=15)
    republica = models.ForeignKey('Republica', related_name='pessoas', on_delete=models.CASCADE)

    def pagar_conta(self, conta, valor, forma_pagamento):
        return Pagamento.objects.create(
            pessoa=self,
            conta=conta,
            valor_pago=valor,
            forma_pagamento=forma_pagamento
        )

    def verificar_pagamentos_feitos(self):
        return self.pagamentos.all()

    def __str__(self):
        return self.nome


class Conta(models.Model):
    republica = models.ForeignKey('Republica', related_name='contas', on_delete=models.CASCADE)
    nome_conta = models.CharField(max_length=100)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    status = models.CharField(max_length=50)

    def registrar_pagamento(self, pagamento):
        pagamento.conta = self
        pagamento.save()

    def verificar_status(self):
        return self.status

    def __str__(self):
        return f"{self.nome_conta} - R$ {self.valor}"


class Pagamento(models.Model):
    pessoa = models.ForeignKey('Pessoa', related_name='pagamentos', on_delete=models.CASCADE)
    conta = models.ForeignKey('Conta', related_name='pagamentos', on_delete=models.CASCADE)
    valor_pago = models.FloatField()
    data_pagamento = models.DateField(auto_now_add=True)
    forma_pagamento = models.CharField(max_length=50)

    def verificar_sucesso_do_pagamento(self):
        return self.valor_pago >= self.conta.valor

    def __str__(self):
        return f"{self.pessoa.nome} pagou R$ {self.valor_pago} em {self.data_pagamento}"