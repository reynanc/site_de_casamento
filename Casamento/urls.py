from django.contrib import admin
from django.urls import path
from app_casamento import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cerimonia-espaco/', views.cerimonia_espaco, name='cerimonia_espaco'),
    path('confirmar-presenca/', views.confirmar_presenca, name='confirmar_presenca'),
    path('dicas/', views.dicas, name='dicas'),
    path('lista-presentes/', views.lista_presentes, name='lista_presentes'),
    path('mensagens/', views.mensagens, name='mensagens'),
    path('presentes/comprar/<int:presente_id>/', views.comprar_presente, name='comprar_presente'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)