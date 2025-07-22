from django.utils.deprecation import MiddlewareMixin
from .models import Visitante
from django.utils import timezone
from datetime import timedelta

class VisitanteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        ultima_visita = Visitante.objects.filter(
            ip_address=ip,
            visitado_em__gte=timezone.now() - timedelta(hours=24)
        ).first()
        
        if not ultima_visita:
            Visitante.objects.create(
                ip_address=ip,
                user_agent=user_agent,
                pagina=request.path
            )
        
        return None