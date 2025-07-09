from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Pessoa, Republica

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

        # Novos campos para criar a Pessoa
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        idade = request.POST.get('idade')
        telefone = request.POST.get('telefone')

        # Validação dos campos vazios
        if not all([usuario, email, senha, nome, cpf, idade, telefone]):
            messages.warning(request, 'Preencha todos os campos.')
            return redirect('/auth/cadastro')

        # Verifica se já existe pessoa com esse nome de usuário cadastrado
        user = User.objects.filter(username=usuario).first()
        if user:
            messages.warning(request, 'Já existe uma pessoa com esse nome de usuário.')
            return redirect('/auth/cadastro')
        
        # Verifica se já existe pessoa com esse CPF cadastrado
        pessoa_existente = Pessoa.objects.filter(cpf=cpf).first()
        if pessoa_existente:
            messages.warning(request, 'Já existe uma pessoa com esse CPF.')
            return redirect('/auth/cadastro')

        try:
            # Buscar a única república do sistema
            republica = Republica.objects.first()
            
            if not republica:
                messages.error(request, 'Nenhuma república encontrada no sistema. Entre em contato com o administrador.')
                return redirect('/auth/cadastro')
            
            # Criar o usuário
            user = User.objects.create_user(username=usuario, email=email, password=senha)
            user.first_name = nome  # Salvar o nome no User também
            user.save()

            # Criar a pessoa
            pessoa = Pessoa.objects.create(
                user=user,
                cpf=cpf,
                nome=nome,
                idade=int(idade),
                telefone=telefone,
                republica=republica
            )

            messages.success(request, 'Membro cadastrado com sucesso! Faça login.')
            return redirect('/auth/login')

        except ValueError:
            messages.error(request, 'Idade deve ser um número válido.')
            return redirect('/auth/cadastro')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
            return redirect('/auth/cadastro')

def logout(request):
    logout_django(request)
    messages.info(request, 'Logout realizado com sucesso.')
    return redirect('/auth/login')