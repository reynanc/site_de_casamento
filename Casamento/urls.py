from django.contrib import admin
from django.urls import path
from app_casamento import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cerimonia-espaco/', views.cerimonia_espaco, name='cerimonia_espaco'),
    path('confirmar-presenca/', views.confirmar_presenca, name='confirmar_presenca'),
    path('dicas/', views.dicas, name='dicas'),
    path('lista-presentes/', views.lista_presentes, name='lista_presentes'),
    path('mensagens/', views.mensagens, name='mensagens'),
]
