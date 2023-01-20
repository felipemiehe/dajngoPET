from django.db import models
from django.contrib.auth.models import User
from divulgar.models import Pet



# Create your models here.

class PedidoAdocao(models.Model):
    choices_status = (
        ('AG', 'Aguardando aprovação'),
        ('AP', 'Aprovado'),
        ('R', 'Recusado')
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)    
    data = models.DateTimeField()
    status = models.CharField(max_length=2, choices=choices_status, default='AG')
    donosolicitacao = models.CharField(max_length=30, default='Null')
    

    def __str__(self) -> str:
        return self.pet.nome
