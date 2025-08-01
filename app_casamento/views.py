from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import mercadopago
import json
from .forms import MensagemForm, PartidaForm, PresensaForm, CompraForm
from .models import Mensagem, Convidado, Visitante, Presente, CompraPresente
from .api_mercado_pago import criar_pagamento_presente
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def get_contador_visitantes():

    # Contar visitantes únicos dos últimos 30 dias para evitar acúmulo excessivo
    from datetime import timedelta
    from django.utils import timezone
    
    data_limite = timezone.now() - timedelta(days=30)
    return Visitante.objects.filter(visitado_em__gte=data_limite).count()

def home(request):
    context = {
        'total_visitantes': get_contador_visitantes()
    }
    return render(request, 'home.html', context)

def cerimonia_espaco(request):
    form = PartidaForm()

    context = {
        'form': form,
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
            
            # Enviar email de agradecimento
            if enviar_email_agradecimento(compra):
                messages.success(request, f'Pagamento aprovado! Obrigado por presentear {compra.presente.nome}! Um email de confirmação foi enviado.')
            else:
                messages.success(request, f'Pagamento aprovado! Obrigado por presentear {compra.presente.nome}!')
                
        except CompraPresente.DoesNotExist:
            messages.error(request, 'Compra não encontrada.')
    
    # Filtros e ordenação
    categoria_filtro = request.GET.get('categoria', '')
    ordenar_por = request.GET.get('ordenar', '')
    
    # Mostrar todos os presentes, incluindo os esgotados
    presentes = Presente.objects.all()
    
    # Aplicar filtros
    if categoria_filtro:
        presentes = presentes.filter(categoria=categoria_filtro)

    
    # Aplicar ordenação
    if ordenar_por == 'maior_preco':
        presentes = presentes.order_by('-preco', 'nome')
    elif ordenar_por == 'menor_preco':
        presentes = presentes.order_by('preco', 'nome')
    else:
        presentes = presentes.order_by('categoria', 'nome')
    
    # Agrupar presentes por categoria
    presentes_por_categoria = {}
    for presente in presentes:
        categoria = presente.get_categoria_display()
        if categoria not in presentes_por_categoria:
            presentes_por_categoria[categoria] = []
        presentes_por_categoria[categoria].append(presente)
    
    # Obter todas as categorias para o filtro
    todas_categorias = Presente.CATEGORIA_CHOICES
    
    # Obter valores mínimo e máximo dos preços para os filtros
    from django.db.models import Min, Max
    preco_range = Presente.objects.aggregate(
        preco_minimo=Min('preco'),
        preco_maximo=Max('preco')
    )
    
    context = {
        'presentes_por_categoria': presentes_por_categoria,
        'todas_categorias': todas_categorias,
        'categoria_filtro': categoria_filtro,
        'ordenar_por': ordenar_por,
        'preco_minimo_db': preco_range['preco_minimo'] or 0,
        'preco_maximo_db': preco_range['preco_maximo'] or 1000,
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
                link_retorno = f'https://www.laynan.com.br/lista-presentes/?compra_id={compra.id}&status=approved'
                link_pagamento, id_pagamento = criar_pagamento_presente(presente, link_retorno, compra.id)

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
            
            # Enviar email de agradecimento
            if enviar_email_agradecimento(compra):
                messages.success(request, f'Pagamento aprovado! Obrigado por presentear {compra.presente.nome}! Um email de confirmação foi enviado.')
            else:
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
    # IPs permitidos do Mercado Pago
    allowed_ips = [
        '209.225.49.0/24',
        '216.33.197.0/24', 
        '216.33.196.0/24',
        '209.225.48.0/24'
    ]
    
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
                            try:
                                enviar_email_agradecimento(compra)
                                print(f"Email enviado com sucesso para {compra.email_comprador}")
                            except Exception as email_error:
                                print(f"Erro ao enviar email: {email_error}")
                                
                        elif payment_data['status'] == 'rejected':
                            compra.status = 'rejeitado'
                        elif payment_data['status'] in ['pending', 'in_process']:
                            compra.status = 'pendente'
                        
                        compra.save()
                    except CompraPresente.DoesNotExist:
                        pass
        
        return HttpResponse(status=200)
    except Exception as e:
        print(f"Erro no webhook: {e}")
        return HttpResponse(status=400)

def mensagens(request):
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Obrigado por fazer parte deste momento especial.')
            return redirect('mensagens')
    else:
        form = MensagemForm()
    
    # Buscar todas as mensagens do banco de dados
    mensagens_enviadas = Mensagem.objects.all().order_by('-criado_em')
    
    context = {
        'form': form,
        'mensagens_enviadas': mensagens_enviadas,
        'total_visitantes': get_contador_visitantes()
    }
    
    return render(request, 'mensagens.html', context)


def enviar_email_agradecimento(compra):
    """
    Envia email de agradecimento para o comprador do presente
    """
    try:
        # Contexto para o template do email
        context = {
            'nome_comprador': compra.nome_comprador,
            'presente_nome': compra.presente.nome,
            'presente_preco': compra.presente.preco,
            'mensagem_comprador': compra.mensagem,
        }
        
        # Renderizar template HTML do email
        html_message = render_to_string('email_agradecimento.html', context)
        plain_message = strip_tags(html_message)
        
        # Enviar email
        send_mail(
            subject=f'Obrigado pelo presente: {compra.presente.nome}!',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[compra.email_comprador],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Erro ao enviar email: {e}')
        return False

