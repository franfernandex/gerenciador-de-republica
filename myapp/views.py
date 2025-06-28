from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Conta, Pessoa, Pagamento

# Create your views here.
def principal(request):
    template = loader.get_template('principal.html')


    return HttpResponse(template.render())

def teste(request):
    template = loader.get_template('paginateste.html')
    context = {
        "nome": "José Silva",
        "idade": 30,
        "email": "jose.silva@email.com",
        "telefone": "3333-1234"
    }
    return HttpResponse(template.render(context, request))

def pessoa(request):    #função adicionada
    pessoa = Pessoa.objects.select_related('republica').all()
    template = loader.get_template('pessoas.html')
    context = {
        'pessoas': pessoa
        
    }
    return HttpResponse(template.render(context, request))

def contas(request):         # atualize esta função
    contas = Conta.objects.all().values()
    template = loader.get_template('contas.html')
    context = {
        'contas': contas,
    }
    return HttpResponse(template.render(context, request))

def pagamentos(request):         # atualize esta função
    pagamentos = Pagamento.objects.select_related('pessoa', 'conta').all()
    template = loader.get_template('pagamentos.html')
    context = {
        'pagamentos': pagamentos,
    }
    return HttpResponse(template.render(context, request))