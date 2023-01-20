from django.shortcuts import render, redirect
from divulgar.models import Pet, Raca
from django.contrib.messages import constants
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

@login_required
def listar_pets(request):
    if request.method == 'GET':

        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            # LIKE do SQL __icontains
            pets = pets.filter(cidade__icontains=cidade)
        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        return render(request, 'listar_pet.html', {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter})

################   Cria pedido ADOCAO ###########################

@login_required
def pedido_adocao(request, id_pet):

    pet = Pet.objects.filter(id = id_pet).filter(status='P') 
    usuario= Pet.objects.get(id= id_pet).usser() 
        
    if not pet.exists():
        messages.add_message(request, constants.WARNING,
                             'esse pet já foi adotado')
        return redirect('/adotar')       

    pedido = PedidoAdocao(
        pet=pet.first(),
        usuario=usuario,
        data=datetime.now(),
        donosolicitacao = request.user.username,
    )

    pedido.save()

    messages.add_message(request, constants.SUCCESS,
                         'esse pedido foi relizado com sucesso')

    return redirect('/adotar')

######## PROCESSAR PEDIDO DE ADOÇÂO + EMAIL + MUDA STATUS PET #######

@login_required
def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id = id_pedido)
    pet = Pet.objects.get(id = pedido.pet_id)    

    if status == 'A':                
        pedido.status='AP'
        pet.status = 'A'

        string = '''Olá, sua adoção foi aprovada com sucesso'''

    elif status == 'R':
        string = '''Olá, sua adoção foi recusada'''
        pedido.status='R'
        
    
    pedido.save()
    pet.save()

    email = send_mail(
        'Sua adoção foi processada',
        string,
        'felipe@felipetestando.com.br',
        [pedido.usuario.email,]
    )

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso')


    return redirect('/divulgar/ver_pedido_adocao')


