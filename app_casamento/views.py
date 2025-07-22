from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import mercadopago
import json
from .forms import ConvidadosForm, PartidaForm, PresensaForm, CompraForm
from .models import Convidados, Presencas, Visitante, Presente, CompraPresente
from .api_mercado_pago import criar_pagamento_presente

def get_contador_visitantes():
    """Função para obter o número total de visitantes únicos"""
    return Visitante.objects.count()

def home(request):
    context = {
        'total_visitantes': get_contador_visitantes()
    }
    return render(request, 'home.html', context)

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
    
    context = {
        'form': form,
        'local_evento': local_evento,
        'total_visitantes': get_contador_visitantes()
    }
    
    return render(request, 'cerimonia_espaco.html', context)

def confirmar_presenca(request):
    if request.method == 'POST':
        form = PresensaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua presença foi confirmada com sucesso! Estamos ansiosos para celebrar com você!')
            return redirect('confirmar_presenca')
    else:
        form = PresensaForm()
    
    context = {
        'form': form,
        'total_visitantes': get_contador_visitantes()
    }
    
    return render(request, 'confirmar_presenca.html', context)

def dicas(request):
    context = {
        'total_visitantes': get_contador_visitantes()
    }
    return render(request, 'dicas.html', context)

def lista_presentes(request):
    compra_id = request.GET.get('compra_id')
    status = request.GET.get('status')
    
    if compra_id and status == 'approved':
        try:
            compra = CompraPresente.objects.get(id=compra_id)
            compra.status = 'aprovado'
            compra.save()
            
            # Diminuir quantidade do presente
            if compra.presente.quantidade > 0:
                compra.presente.quantidade -= 1
                compra.presente.save()
            
            messages.success(request, f'Pagamento aprovado! Obrigado por presentear {compra.presente.nome}!')
        except CompraPresente.DoesNotExist:
            messages.error(request, 'Compra não encontrada.')
    
    # Mostrar todos os presentes, incluindo os esgotados
    presentes = Presente.objects.all().order_by('categoria', 'nome')
    
    # Agrupar presentes por categoria
    presentes_por_categoria = {}
    for presente in presentes:
        categoria = presente.get_categoria_display()
        if categoria not in presentes_por_categoria:
            presentes_por_categoria[categoria] = []
        presentes_por_categoria[categoria].append(presente)
    
    context = {
        'presentes_por_categoria': presentes_por_categoria,
        'total_visitantes': get_contador_visitantes()
    }
    return render(request, 'lista_presentes.html', context)

def comprar_presente(request, presente_id):
    presente = get_object_or_404(Presente, id=presente_id, quantidade__gt=0)
    
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.presente = presente
            compra.save()
            
            try:
                link_retorno = f'http://127.0.0.1:8000/lista-presentes/?compra_id={compra.id}&status=approved'
                link_pagamento, id_pagamento = criar_pagamento_presente(presente, link_retorno)

                compra.preference_id = id_pagamento
                compra.save()

                return redirect(link_pagamento) 
                
            except Exception as e:
                messages.error(request, f'Erro ao processar pagamento: {str(e)}')
    else:
        form = CompraForm()
    
    context = {
        'presente': presente,
        'form': form,
        'total_visitantes': get_contador_visitantes()
    }
    return render(request, 'comprar_presente.html', context)

def pagamento_sucesso(request):
    compra_id = request.GET.get('compra_id')
    if compra_id:
        try:
            compra = CompraPresente.objects.get(id=compra_id)
            compra.status = 'aprovado'
            compra.save()
            
            # Diminuir quantidade do presente
            if compra.presente.quantidade > 0:
                compra.presente.quantidade -= 1
                compra.presente.save()
            
            messages.success(request, f'Pagamento aprovado! Obrigado por presentear {compra.presente.nome}!')
        except CompraPresente.DoesNotExist:
            messages.error(request, 'Compra não encontrada.')
    
    return render(request, 'pagamento_resultado.html', {
        'status': 'sucesso',
        'total_visitantes': get_contador_visitantes()
    })

def pagamento_falha(request):
    compra_id = request.GET.get('compra_id')
    if compra_id:
        try:
            compra = CompraPresente.objects.get(id=compra_id)
            compra.status = 'rejeitado'
            compra.save()
        except CompraPresente.DoesNotExist:
            pass
    
    messages.error(request, 'Pagamento não foi aprovado. Tente novamente.')
    return render(request, 'pagamento_resultado.html', {
        'status': 'falha',
        'total_visitantes': get_contador_visitantes()
    })

def pagamento_pendente(request):
    compra_id = request.GET.get('compra_id')
    if compra_id:
        try:
            compra = CompraPresente.objects.get(id=compra_id)
            compra.status = 'pendente'
            compra.save()
        except CompraPresente.DoesNotExist:
            pass
    
    messages.info(request, 'Pagamento está sendo processado. Você receberá uma confirmação em breve.')
    return render(request, 'pagamento_resultado.html', {
        'status': 'pendente',
        'total_visitantes': get_contador_visitantes()
    })

@csrf_exempt
@require_POST
def webhook_mercadopago(request):
    try:
        data = json.loads(request.body)
        
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            
            # Configurar SDK
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            
            # Buscar informações do pagamento
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info['status'] == 200:
                payment_data = payment_info['response']
                external_reference = payment_data.get('external_reference')
                
                if external_reference:
                    try:
                        compra = CompraPresente.objects.get(id=external_reference)
                        compra.payment_id = payment_id
                        
                        # Atualizar status baseado no status do pagamento
                        if payment_data['status'] == 'approved':
                            compra.status = 'aprovado'
                            if compra.presente.quantidade > 0:
                                compra.presente.quantidade -= 1
                                compra.presente.save()
                        elif payment_data['status'] == 'rejected':
                            compra.status = 'rejeitado'
                        elif payment_data['status'] in ['pending', 'in_process']:
                            compra.status = 'pendente'
                        
                        compra.save()
                    except CompraPresente.DoesNotExist:
                        pass
        
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)

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
    
    context = {
        'form': form,
        'mensagens_enviadas': mensagens_enviadas,
        'total_visitantes': get_contador_visitantes()
    }
    
    return render(request, 'mensagens.html', context)

