from django.utils.deprecation import MiddlewareMixin
from .models import Visitante
from django.utils import timezone
from datetime import timedelta
import re

class VisitanteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verificar se já foi contado nesta sessão
        if not request.session.get('visitante_contado', False):
            # Lista de IPs a serem ignorados
            ips_ignorados = [
                '209.225.49.0/24',
                '216.33.197.0/24',
                '216.33.196.0/24',
                '209.225.48.0/24',
                '127.0.0.1',
                'localhost',
                '18.215.140.160',  # Mercado Pago webhook
                '18.213.114.129',  # Mercado Pago webhook
                '54.88.218.97',    # Mercado Pago webhook
                '18.206.34.84',    # Mercado Pago webhook
                '47.91.29.151',    # Outros serviços
                '94.247.172.129',  # Outros serviços
                '17.241.227.73',   # Outros serviços
                '210.64.24.100',   # Outros serviços
                '111.231.1.45',    # Outros serviços
                '136.0.74.145',    # Outros serviços
                '101.199.254.231', # Outros serviços
                '101.199.254.239', # Outros serviços
                '101.199.254.209', # Outros serviços
                '101.199.254.242'  # Outros serviços
            ]

            # Lista de User-Agents a serem ignorados (bots e crawlers)
            user_agents_ignorados = [
                r'bot',
                r'crawler',
                r'spider',
                r'python',
                r'curl',
                r'requests',
                r'mercadopago',
                r'django',
                r'apache',
                r'nginx',
                r'check',
                r'monitor',
                r'health',
                r'status',
                r'probe',
                r'scan',
                r'test',
                r'php',
                r'go-http',
                r'java',
                r'wget',
                r'ruby',
                r'check_http',
                r'zgrab',
                r'chrome-lighthouse',
                r'pagespeed',
                r'mozilla/5\.0$',  # User-agents que terminam abruptamente
                r'^mozilla$',      # User-agents muito genéricos
                r'^postman',       # Ferramentas de teste de API
                r'^$'              # User-agent vazio
            ]

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

            # Lista de caminhos a serem ignorados
            caminhos_ignorados = [
                r'^/robots\.txt$',
                r'^/sitemap\.xml$',
                r'^/favicon\.ico$',
                r'^/wp-includes/',
                r'^/config\.json$',
                r'^/webhook/',
                r'^/.well-known/',
                r'^/license\.txt$',
                r'^/readme\.txt$',
                r'^/admin/',
                r'^/static/',
                r'^/media/'
            ]

            # Verificar se o caminho deve ser ignorado
            if any(re.match(pattern, request.path) for pattern in caminhos_ignorados):
                return None

            # Verificar se o IP deve ser ignorado
            if any(ip.startswith(ignored_ip.replace('/24', '')) for ignored_ip in ips_ignorados):
                return None

            # Verificar se o User-Agent deve ser ignorado
            if any(re.search(pattern, user_agent, re.IGNORECASE) for pattern in user_agents_ignorados):
                return None
            
            # Verificar se já existe visitante com mesmo IP nas últimas 6 horas
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