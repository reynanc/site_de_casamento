from django.db import models
from django.utils import timezone
import uuid

class Mensagem(models.Model):
    id = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name="Criado em")
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    mensagem = models.TextField(verbose_name="Mensagem", blank=True, null=True)

    def __str__(self):
        return self.nome

class Convidado(models.Model):
    id = models.AutoField(primary_key=True)
    criado_em = models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name="Criado em")
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome")
    telefone = models.CharField(max_length=15, verbose_name="Número de Telefone", null=True, blank=True)
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)

    qtd_adultos = models.PositiveIntegerField(default=1, verbose_name="Quantidade de Adultos")
    nomes_adultos = models.TextField(blank=True, null=True, verbose_name="Nomes dos Adultos")
    qtd_criancas = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Crianças")
    nomes_criancas = models.TextField(blank=True, null=True, verbose_name="Nomes das Crianças")
    qtd_adolescentes = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Adolescentes")
    nomes_adolescentes = models.TextField(blank=True, null=True, verbose_name="Nomes dos Adolescentes") 

    def __str__(self):
        return self.nome

class Visitante(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    visitado_em = models.DateTimeField(default=timezone.now)
    pagina = models.CharField(max_length=255, default='/')
    
    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
    
    def __str__(self):
        return f"{self.ip_address} - {self.visitado_em}"

class Presente(models.Model):
    CATEGORIA_CHOICES = [
        ('casa', 'Casa'),
        ('sala', 'Sala'),
        ('cozinha', 'Cozinha'),
        ('quarto', 'Quarto'),
        ('banheiro', 'Banheiro'),
        ('decoracao', 'Decoração'),
        ('eletronicos', 'Eletrônicos'),
        ('outros', 'Outros'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Presente")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoria")
    imagem = models.ImageField(upload_to='presentes/', verbose_name="Imagem", blank=True, null=True)
    link_produto = models.URLField(verbose_name="Link do Produto", blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade Disponível")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Presente"
        verbose_name_plural = "Presentes"
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
    
    @property
    def disponivel(self):
        """Retorna True se há quantidade disponível"""
        return self.quantidade > 0

class CompraPresente(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presente = models.ForeignKey(Presente, on_delete=models.CASCADE, verbose_name="Presente")
    nome_comprador = models.CharField(max_length=100, verbose_name="Nome do Comprador")
    email_comprador = models.EmailField(verbose_name="E-mail do Comprador")
    telefone_comprador = models.CharField(max_length=15, verbose_name="Telefone", blank=True, null=True)
    mensagem = models.TextField(verbose_name="Mensagem para os Noivos", blank=True, null=True)
    
    # Dados do Mercado Pago
    payment_id = models.CharField(max_length=100, verbose_name="ID do Pagamento", blank=True, null=True)
    preference_id = models.CharField(max_length=100, verbose_name="ID da Preferência", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Compra de Presente"
        verbose_name_plural = "Compras de Presentes"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.nome_comprador} - {self.presente.nome}"

class FotoCarrosel(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título", blank=True, null=True)
    imagem = models.ImageField(upload_to='carrosel/', verbose_name="Imagem", blank=True, null=True)
    ordem = models.PositiveIntegerField(default=1, verbose_name="Ordem", help_text="Ordem em que a foto aparecerá no carrossel")
    ativa = models.BooleanField(default=True, verbose_name="Ativa", help_text="Se marcado, a foto será exibida no carrossel")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    class Meta:
        verbose_name = "Foto do Carrosel"
        verbose_name_plural = "Fotos do Carrosel"
        ordering = ['ordem', 'criado_em']

    def __str__(self):
        return f"{self.titulo}"

