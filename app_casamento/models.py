from django.db import models
from django.utils import timezone

class Convidados(models.Model):
    id = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name="Criado em")
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    mensagem = models.TextField(verbose_name="Mensagem", blank=True, null=True)

    def __str__(self):
        return self.nome

class Presencas(models.Model):
    id = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name="Criado em")
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome")
    telefone = models.CharField(max_length=15, verbose_name="Número de Telefone", null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)

    qtd_adultos = models.PositiveIntegerField(default=1, verbose_name="Quantidade de Adultos")
    nomes_adultos = models.TextField(blank=True, null=True, verbose_name="Nomes dos Adultos")
    qtd_criancas = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Crianças")
    nomes_criancas = models.TextField(blank=True, null=True, verbose_name="Nomes das Crianças")

    def __str__(self):
        return self.nome
