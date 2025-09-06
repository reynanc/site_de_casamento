from django.contrib import admin
from .models import Mensagem, Convidado
from .models import Visitante
from .models import Presente, CompraPresente, FotoCarrosel

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('nome', 'email')
    readonly_fields = ('criado_em',)
    ordering = ('-criado_em',)

    fieldsets = (
        ('Informações do Mensagem', {
            'fields': ('nome', 'email')
        }),
        ('Mensagem', {
            'fields': ('mensagem',)
        }),
        ('Timestamps', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'qtd_adultos', 'qtd_criancas', 'criado_em')
    list_filter = ('criado_em', 'qtd_adultos', 'qtd_criancas')
    search_fields = ('nome', 'email', 'telefone', 'nomes_adultos', 'nomes_criancas')
    readonly_fields = ('criado_em',)
    ordering = ('-criado_em',)

    fieldsets = (
        ('Informações do Mensagem', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Acompanhantes', {
            'fields': ('qtd_adultos', 'nomes_adultos','qtd_adolescentes', 'nomes_adolescentes', 'qtd_criancas', 'nomes_criancas')
        }),
        ('Timestamps', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'visitado_em', 'pagina']
    list_filter = ['visitado_em', 'pagina']
    readonly_fields = ['ip_address', 'user_agent', 'visitado_em', 'pagina']
    ordering = ['-visitado_em']


@admin.register(Presente)
class PresenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'quantidade', 'criado_em')
    list_filter = ('categoria', 'quantidade', 'criado_em')
    search_fields = ('nome', 'descricao')
    list_editable = ('quantidade',)
    ordering = ('categoria', 'nome')

@admin.register(CompraPresente)
class CompraPresenteAdmin(admin.ModelAdmin):
    list_display = ('nome_comprador', 'presente', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome_comprador', 'email_comprador', 'presente__nome')
    readonly_fields = ('id', 'payment_id', 'preference_id', 'criado_em', 'atualizado_em')
    ordering = ('-criado_em',)

@admin.register(FotoCarrosel)
class FotoCarroselAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'ativa', 'criado_em')
    list_filter = ('ativa', 'criado_em')
    search_fields = ('titulo',)
    list_editable = ('ordem', 'ativa')
    ordering = ('ordem', 'criado_em')

    fieldsets = (
        ('Informações da Foto', {
            'fields': ('titulo', 'imagem')
        }),
        ('Configurações', {
            'fields': ('ordem', 'ativa')
        }),
        ('Timestamps', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return ('criado_em',)
