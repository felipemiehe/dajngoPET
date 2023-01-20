from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Tag, Raca, Pet
from django.contrib import messages
from django.contrib.messages import constants
from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@login_required
def novo_pet(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas})
    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')  # pega mais que 1 atributo
        raca = request.POST.get('raca')

        # class PET
        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
        )

        pet.save()

        # Add tags many to many
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)

        pet.save()

    return redirect('/divulgar/seus_pet')


# --------- LISTAR PET ----- ##########!->
@login_required
def seus_pet(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets': pets})


# --------- REMOVER PET ----- ##########!->
@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id = id)
    try:
        if not pet.usuario == request.user:
            messages.add_message(
                request, constants.WARNING, 'Esse pet não é seu!')
            return redirect('/divulgar/seus_pet')
        # DELETE
        pet.delete()
        messages.add_message(request, constants.SUCCESS,
                             'Removido com sucesso')
        return redirect('/divulgar/seus_pet')
    except:
        messages.add_message(request, constants.WARNING, 'Algo deu errado!')     
        return redirect('/divulgar/seus_pet')

# --------- VER PET----- ##########!->


@login_required
def ver_pet(request, id):
    if request.method == 'GET':
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet': pet})

# --------- REMOVER PEDIDO DE ADOÇÂO ----- ##########!->


@login_required
def ver_pedido_adocao(request):
    if request.method == 'GET':
        pedidos = PedidoAdocao.objects.filter(
            usuario=request.user).filter(status='AG')
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})

# --------- GRÁFICOS PAGE ----- ##########!->


def dashboard(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')

# --------- API GRAFICOS ----- ##########!->


@csrf_exempt
def api_adocoes_por_raca(reqquest):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(
            pet__raca=raca).filter(status = 'AP').count()  # __ pegar outra coluna
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas
            }
    return JsonResponse(data)