from django.utils.deprecation import MiddlewareMixin
from .models import Visitante
from django.utils import timezone
from datetime import timedelta

class VisitanteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verificar se já foi contado nesta sessão
        if not request.session.get('visitante_contado', False):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Verificar se já existe visitante com mesmo IP nas últimas 6 horas
            # (para evitar contagem excessiva de IPs dinâmicos)
            ultima_visita = Visitante.objects.filter(
                ip_address=ip,
                visitado_em__gte=timezone.now() - timedelta(hours=6)
            ).first()
            
            if not ultima_visita:
                Visitante.objects.create(
                    ip_address=ip,
                    user_agent=user_agent,
                    pagina=request.path
                )
            
            # Marcar como contado nesta sessão
            request.session['visitante_contado'] = True
            request.session['primeira_visita'] = timezone.now().isoformat()
        
        return None