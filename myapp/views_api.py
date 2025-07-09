from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Republica, Pessoa, Conta, Pagamento
from .serializers import RepublicaSerializer, PessoaSerializer, ContaSerializer, PagamentoSerializer

# Obter a pessoa logada
def get_logged_in_pessoa(request):
    """
    Retorna a instância de Pessoa associada ao usuário logado.
    Assume que o modelo Pessoa tem um OneToOneField para User.
    """
    if not request.user.is_authenticated:
        return None
    try:
        return Pessoa.objects.get(user=request.user)
    except Pessoa.DoesNotExist:
        return None

class RepublicaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para listar repúblicas (somente leitura).
    Pode ser acessado por qualquer usuário autenticado.
    """
    queryset = Republica.objects.all()
    serializer_class = RepublicaSerializer
    permission_classes = [IsAuthenticated]

class PessoaViewSet(viewsets.ModelViewSet):
    """
    API para listar e gerenciar Pessoas (membros) da república do usuário logado.
    """
    serializer_class = PessoaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as Pessoas que pertencem à república do usuário logado.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if pessoa_logada:
            return Pessoa.objects.filter(republica=pessoa_logada.republica).order_by('nome')
        return Pessoa.objects.none() # Nenhuma pessoa se o usuário não estiver associado a uma república

    def perform_create(self, serializer):
        """
        Ao criar uma nova Pessoa, associa à república do usuário logado.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if pessoa_logada:
            # Não associamos um User aqui, pois é um cadastro de membro, não de usuário do sistema
            serializer.save(republica=pessoa_logada.republica)
        else:
            raise serializers.ValidationError("Usuário não associado a uma república.")

class ContaViewSet(viewsets.ModelViewSet):
    """
    API para listar e gerenciar Contas da república do usuário logado.
    """
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as Contas que pertencem à república do usuário logado.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if pessoa_logada:
            return Conta.objects.filter(republica=pessoa_logada.republica).order_by('-data_vencimento')
        return Conta.objects.none()

    def perform_create(self, serializer):
        """
        Ao criar uma nova Conta, associa à república do usuário logado
        e define 'paga' como False por padrão.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if pessoa_logada:
            serializer.save(republica=pessoa_logada.republica, paga=False)
        else:
            raise serializers.ValidationError("Usuário não associado a uma república.")

class PagamentoViewSet(viewsets.ModelViewSet):
    """
    API para listar e gerenciar Pagamentos da república do usuário logado.
    """
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas os Pagamentos que pertencem à república do usuário logado.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if pessoa_logada:
            # Filtra pagamentos onde a conta pertence à república do usuário
            return Pagamento.objects.filter(conta__republica=pessoa_logada.republica).order_by('-data_pagamento')
        return Pagamento.objects.none()

    def perform_create(self, serializer):
        """
        Ao criar um novo Pagamento:
        - Associa à Pessoa logada.
        - Define o valor_pago como o valor total da conta.
        - Marca a conta como paga (lógica já no save do modelo Pagamento).
        - Verifica se a conta já foi paga ou se a pessoa já pagou.
        """
        pessoa_logada = get_logged_in_pessoa(self.request)
        if not pessoa_logada:
            raise serializers.ValidationError("Usuário não associado a uma república.")

        conta_id = self.request.data.get('conta')
        if not conta_id:
            raise serializers.ValidationError({"conta": "O campo 'conta' é obrigatório."})

        try:
            conta = get_object_or_404(Conta, id=conta_id)
        except:
            raise serializers.ValidationError({"conta": "Conta não encontrada."})

        if conta.paga:
            raise serializers.ValidationError("Esta conta já foi paga.")

        if Pagamento.objects.filter(pessoa=pessoa_logada, conta=conta).exists():
            raise serializers.ValidationError("Você já pagou essa conta.")

        # O valor_pago será o valor da conta.
        serializer.save(pessoa=pessoa_logada, valor_pago=conta.valor)
