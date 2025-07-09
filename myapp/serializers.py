from rest_framework import serializers
from .models import Republica, Pessoa, Conta, Pagamento, User # Importe User aqui também

# Serializer para o modelo User (para incluir informações básicas do usuário)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Serializer para o modelo Republica
class RepublicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Republica
        fields = '__all__' # Inclui todos os campos do modelo

# Serializer para o modelo Pessoa
class PessoaSerializer(serializers.ModelSerializer):
    republica_nome = serializers.CharField(source='republica.nome', read_only=True)
    user = UserSerializer(read_only=True) # Inclui o serializer do User aninhado

    class Meta:
        model = Pessoa
        fields = ['id', 'user', 'cpf', 'nome', 'idade', 'telefone', 'republica', 'republica_nome']
        read_only_fields = ['user'] # O campo user será preenchido automaticamente

# Serializer para o modelo Conta
class ContaSerializer(serializers.ModelSerializer):
    republica_nome = serializers.CharField(source='republica.nome', read_only=True)

    class Meta:
        model = Conta
        fields = ['id', 'republica', 'republica_nome', 'nome_conta', 'valor', 'data_vencimento', 'paga']
        read_only_fields = ['republica', 'paga'] # Republica e paga serão definidos pela lógica da view

# Serializer para o modelo Pagamento
class PagamentoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome', read_only=True)
    conta_nome = serializers.CharField(source='conta.nome_conta', read_only=True)
    conta_valor = serializers.DecimalField(source='conta.valor', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pagamento
        fields = ['id', 'pessoa', 'pessoa_nome', 'conta', 'conta_nome', 'conta_valor', 'valor_pago', 'data_pagamento']
        read_only_fields = ['pessoa', 'valor_pago', 'data_pagamento'] # Pessoa, valor_pago e data_pagamento serão definidos pela lógica da view
