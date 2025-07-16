from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConvidadosForm, PartidaForm
from .models import Convidados

def home(request):
    return render(request, 'home.html')

def cerimonia_espaco(request):
    form = PartidaForm()
    
    # Coordenadas do local do evento (Espaço Bouganville)
    local_evento = {
        'nome': 'Espaço Bouganville',
        'lat': -23.123456,  # Substitua pelas coordenadas reais
        'lng': -46.789012,  # Substitua pelas coordenadas reais
        'endereco': 'Endereço completo do Espaço Bouganville',  # Substitua pelo endereço real
        'data': '13 de dezembro de 2025'
    }
    
    return render(request, 'cerimonia_espaco.html', {
        'form': form,
        'local_evento': local_evento
    })

def confirmar_presenca(request):
    return render(request, 'confirmar_presenca.html')

def dicas(request):
    return render(request, 'dicas.html')

def lista_presentes(request):
    return render(request, 'lista_presentes.html')

def mensagens(request):
    if request.method == 'POST':
        form = ConvidadosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Obrigado por fazer parte deste momento especial.')
            return redirect('mensagens')
    else:
        form = ConvidadosForm()
    
    # Buscar todas as mensagens do banco de dados
    mensagens_enviadas = Convidados.objects.all().order_by('-criado_em')
    
    return render(request, 'mensagens.html', {
        'form': form,
        'mensagens_enviadas': mensagens_enviadas
    })
