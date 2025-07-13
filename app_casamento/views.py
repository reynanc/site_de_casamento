from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def cerimonia_espaco(request):
    return render(request, 'cerimonia_espaco.html')

def confirmar_presenca(request):
    return render(request, 'confirmar_presenca.html')

def dicas(request):
    return render(request, 'dicas.html')

def lista_presentes(request):
    return render(request, 'lista_presentes.html')

def mensagens(request):
    return render(request, 'mensagens.html')
