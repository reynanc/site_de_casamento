from django import forms
from .models import Convidados

class ConvidadosForm(forms.ModelForm):
    class Meta:
        model = Convidados
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'E-mail'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200 resize-none',
                'placeholder': 'Mensagem',
                'rows': 6,
                'maxlength': 2000
            })
        }
        labels = {
            'nome': 'Nome completo',
            'email': 'E-mail',
            'mensagem': 'Mensagem'
        }

class PartidaForm(forms.Form):
    endereco = forms.CharField(
        label='Local de partida',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
            'placeholder': 'Digite seu endereço de origem',
            'id': 'endereco-partida'
        })
    )