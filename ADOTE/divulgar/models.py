from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Raca(models.Model):
    raca = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.raca


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.tag


class Pet(models.Model):

    choices_status = (("P", 'Para adoção'),
                      ('A', 'Adotado'))

    # POSSO USAR CASCADE PARA DELATAR todos pets do usuário , forignKey releção 1 para muitos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    telefone = models.CharField(max_length=14)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)  # manytomany é muitos paras muitos
    status = models.CharField(
        max_length=1, choices=choices_status, default='P')
    # lembra de confiugar o settings # MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # MEDIA_URL = '/media/' #import os
    foto = models.ImageField(upload_to="fotos_pets")

    def __str__(self) -> str:
        return self.nome
        
    def usser(self):
        return self.usuario

    def usserNome(self):
        return self.usuario.username


    
        

    
