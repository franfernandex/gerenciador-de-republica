from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        if user:
            login_django(request, user) 
            return HttpResponse('Autenticado')
        else:
            return HttpResponse('Usuario ou Senha inválidos')
        

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else: #senão será via método "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=usuario).first()
        if user:
            return HttpResponse('Já existe um usuário com esse username')

        # se não existir usuário com esse nome cria e salva o mesmo.
        user = User.objects.create_user(username=usuario, email=email, password=senha)
        user.save()

        return HttpResponse('Usuário cadastrado com sucesso')
    
def logout(request):
    logout_django(request)
    return HttpResponse('Usuario deslogado do sistema!')