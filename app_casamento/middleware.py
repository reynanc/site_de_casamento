import re
import hashlib
from datetime import timedelta
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import Visitante

class VisitanteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Já foi contado nesta sessão
        if request.session.get('visitante_contado', False):
            return None

        # Ignorar rotas específicas
        caminhos_ignorados = [
            r'^/robots\.txt$', r'^/sitemap\.xml$', r'^/favicon\.ico$',
            r'^/wp-includes/', r'^/config\.json$', r'^/webhook/',
            r'^/.well-known/', r'^/license\.txt$', r'^/readme\.txt$',
            r'^/admin/', r'^/static/', r'^/media/'
        ]
        if any(re.match(p, request.path) for p in caminhos_ignorados):
            return None

        # IP do visitante
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()

        # User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # Ignorar User-Agents suspeitos (bots, crawlers, testes)
        if re.search(r'bot|spider|crawl|scrapy|httpclient|python|wget|curl|go-http|java|node|lighthouse|probe|scan|postman', user_agent):
            return None

        # Criar hash único de IP + User-Agent
        hash_key = hashlib.md5(f"{ip}-{user_agent}".encode()).hexdigest()

        # Verificar se já foi registrado nas últimas 6 horas
        limite_tempo = timezone.now() - timedelta(hours=6)
        if Visitante.objects.filter(hash_id=hash_key, visitado_em__gte=limite_tempo).exists():
            return None

        # Criar registro de visitante
        Visitante.objects.create(
            ip_address=ip,
            user_agent=user_agent,
            pagina=request.path,
            hash_id=hash_key
        )

        # Marcar visitante como contado nesta sessão
        request.session['visitante_contado'] = True
        request.session['primeira_visita'] = timezone.now().isoformat()
        return None
