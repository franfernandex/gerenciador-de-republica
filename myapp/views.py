from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Conta, Pessoa, Pagamento, Republica
from .forms import PagamentoForm
from datetime import datetime


# Create your views here.

@login_required
def pagina_restrita(request):
    return render(request, 'principal.html')


def principal(request):
    return render(request, 'principal.html')
   

@login_required
def pessoa(request):
    pessoa = Pessoa.objects.select_related('republica').all()
    template = loader.get_template('pessoas.html')
    context = {
        'pessoas': pessoa
    }
    return HttpResponse(template.render(context, request))


@login_required
def contas(request):
    contas = Conta.objects.all().values()
    template = loader.get_template('contas.html')
    context = {
        'contas': contas,
    }
    return HttpResponse(template.render(context, request))


@login_required
def pagamentos(request):
    pagamentos = Pagamento.objects.select_related('pessoa', 'conta').all()
    template = loader.get_template('pagamentos.html')
    context = {
        'pagamentos': pagamentos,
    }
    return HttpResponse(template.render(context, request))


@login_required
def cadastrar_conta(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_conta.html')
    
    else:   # POST
        nome_conta = request.POST.get('nome_conta')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')

        # Verifica se todos os campos foram preenchidos
        if not all([nome_conta, valor, data_vencimento]):

            messages.warning(request, "Preencha todos os campos para cadastrar uma conta")
            return redirect('cadastrar_conta')

        try:
            # Converte o campo para decimal
            valor_decimal = float(valor.replace(',' , '.'))

            # Converte para data
            data_venc = datetime.strptime(data_vencimento, '%Y-%m-%d').date()

            # Buscas pessoa logada
            pessoa_logada = Pessoa.objects.filter(nome=request.user.first_name).first()

            if not pessoa_logada:
                messages.error(request, 'É necessário estar logado para cadastrar uma conta')
                return redirect('cadastrar_conta')

            # Criar a conta
            conta = Conta.objects.create(
                nome_conta = nome_conta,
                valor = valor_decimal,
                data_vencimento = data_venc,
                republica = pessoa_logada.republica  # Usa a república da pessoa
            )

            messages.success(request, f'Conta {nome_conta} cadastrada com sucesso')
            return redirect('contas')

        except ValueError:
            messages.error(request, 'Valor inválido')
            return redirect('cadastrar_conta')
        
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar conta: {str(e)}')
            return redirect('cadastrar_conta')


@login_required
def adicionar_pagamento(request):
    if request.method == 'GET':
        # Buscas pessoa logada
        pessoa_logada = Pessoa.objects.filter(nome=request.user.first_name).first()

        if not pessoa_logada:
            messages.error(request, 'É necessário estar logado para cadastrar um pagamento')
            return redirect('pagamentos')
        
        # Buscas contas não pagas
        contas_disponiveis = Conta.objects.filter(paga=False)

        context = {
            'pessoa': pessoa_logada,
            'contas_disponiveis': contas_disponiveis
        }
        return render(request, 'adicionar_pagamento.html', context)

    else: #POST
        conta_id = request.POST.get('conta')

        if not conta_id:
            messages.error(request, 'Selecione uma conta')
            return redirect('adicionar_pagamento')

        try:
            # Buscas pessoa logada
            pessoa_logada = Pessoa.objects.filter(nome=request.user.first_name).first()

            if not pessoa_logada:
                messages.error(request, 'Pessoa não encontrada')
                return redirect('pagamentos')
            
            # Buscas a conta
            conta = get_object_or_404(Conta, id=conta_id)

            # Verificar se a conta ja foi paga
            if conta.paga:
                messages.error(request, 'Esta conta já foi paga')
                return redirect('pagamentos')
            
            # Verificar se a pessoa ja pagou essa conta
            if Pagamento.objects.filter(pessoa=pessoa_logada, conta=conta).exists():
                messages.error(request, 'Você já pagou essa conta')
                return redirect('pagamentos')

            # Criar o pagamento
            pagamento = Pagamento.objects.create(
                pessoa = pessoa_logada,
                conta = conta,
                valor_pago = conta.valor # Sempre o valor total da respectiva conta
            )

            messages.success(request, f'Pagamento de R$ {conta.valor} registrado com sucesso')
            return redirect('pagamentos')

        except Exception as e:
            messages.error(request, f'Erro ao registrar o pagamento: {str(e)}')
            return redirect('adicionar_pagamento')
