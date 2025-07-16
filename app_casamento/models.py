from django.db import models

class Convidados(models.Model):
    id = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField(max_length=2000)

    def __str__(self):
        return self.nome
