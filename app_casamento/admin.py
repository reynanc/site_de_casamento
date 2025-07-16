from django.contrib import admin
from .models import Convidados, Presencas

@admin.register(Convidados)
class ConvidadosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('nome', 'email')
    readonly_fields = ('criado_em',)
    ordering = ('-criado_em',)

    fieldsets = (
        ('Informações do Convidado', {
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

@admin.register(Presencas)
class PresencasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'qtd_adultos', 'qtd_criancas', 'criado_em')
    list_filter = ('criado_em', 'qtd_adultos', 'qtd_criancas')
    search_fields = ('nome', 'email', 'telefone', 'nomes_adultos', 'nomes_criancas')
    readonly_fields = ('criado_em',)
    ordering = ('-criado_em',)

    fieldsets = (
        ('Informações do Convidado', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Acompanhantes', {
            'fields': ('qtd_adultos', 'nomes_adultos', 'qtd_criancas', 'nomes_criancas')
        }),
        ('Timestamps', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
