from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout



# CADASTRO --########################################!>
def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(str(confirmar_senha.strip())) == 0 or len(str(senha.strip())) == 0 or len(str(email.strip())) == 0 or len(str(nome.strip())) == 0:
            messages.add_message(request, constants.ERROR,
                                 'Preencha todos os campos')
            return render(request, 'cadastro.html')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'Digite senhas iguais')
            return render(request, 'cadastro.html')
        try:
            # sucesso
            messages.add_message(request, constants.SUCCESS,
                                 'Cadastro realizado com sucesso!')
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            return render(request, 'login.html')

        except:
            # erro
            messages.add_message(request, constants.ERROR,
                                 'Usuário já existe ou erro de sistema')
            return render(request, 'cadastro.html')


# LOGIN --########################################!>
def logar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(
            username=nome,
            password=senha
        )

        if user != None:
            login(request, user )
            return redirect('/divulgar/novo_pet')
        else:
            messages.add_message(request, constants.ERROR,
                                 'Usuário ou senha incorretos')
            return render(request, 'login.html')

# LOGOUT --########################################!>
def sair(request):
    logout(request)
    return redirect('/login') 

        
