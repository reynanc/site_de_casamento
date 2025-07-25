from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app_casamento.models import Visitante

class Command(BaseCommand):
    help = 'Remove visitantes com mais de 30 dias'
    
    def handle(self, *args, **options):
        data_limite = timezone.now() - timedelta(days=30)
        visitantes_removidos = Visitante.objects.filter(
            visitado_em__lt=data_limite
        ).delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Removidos {visitantes_removidos} visitantes antigos'
            )
        )