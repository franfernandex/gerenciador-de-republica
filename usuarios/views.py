from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

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
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('/') # Redireciona para a página principal
        
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('/auth/login')
        

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    else: # Senão será via método "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Validação dos campos vazios
        if not usuario or not email or not senha:
            messages.warning(request, 'Preencha todos os campos.')
            return redirect('/auth/cadastro')

        # Verifica se já existe usuário
        user = User.objects.filter(username=usuario).first()
        if user:
            messages.warning(request, 'Já existe um usuário com esse nome de usuário.')
            return redirect('/auth/cadastro')

        # Se não existir usuário com esse nome cria e salva o mesmo.
        user = User.objects.create_user(username=usuario, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
        return redirect('/auth/login')

def logout(request):
    logout_django(request)
    messages.info(request, 'Logout realizado com sucesso.')
    return redirect('/auth/login')