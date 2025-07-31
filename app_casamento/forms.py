from django import forms
from .models import Mensagem, Convidado, CompraPresente


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Nome *'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'E-mail'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200 resize-none',
                'placeholder': 'Mensagem *',
                'rows': 6,
                'maxlength': 2000
            })
        }
        labels = {
            'nome': '*Nome',
            'email': 'E-mail',
            'mensagem': '*Mensagem'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields
        self.fields['nome'].required = True
        self.fields['mensagem'].required = True


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


class PresensaForm(forms.ModelForm):
    class Meta:
        model = Convidado
        fields = ['nome', 'email', 'telefone', 'qtd_adultos', 'nomes_adultos', 'qtd_criancas', 'nomes_criancas', 'qtd_adolescentes', 'nomes_adolescentes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Nome *'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'E-mail'
            }),
            'telefone': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                    'placeholder': '(81) 98888-8888 (opcional)'}),
            'qtd_adultos': forms.NumberInput(attrs={
                'class': 'w-20 px-3 py-2 border border-gray-300 rounded-lg text-center',
                'min': '1',
                'max': '10',
                'readonly': True,
            }),
            'nomes_adultos': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Digite o nome de cada acompanhante adulto (um por linha)',
                'rows': 3
            }),
            'qtd_criancas': forms.NumberInput(attrs={
                'class': 'w-20 px-3 py-2 border border-gray-300 rounded-lg text-center',
                'min': '0',
                'max': '10',
                'readonly': True,
            }),
            'nomes_criancas': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Digite o nome de cada criança (um por linha)',
                'rows': 3
            }),
            'qtd_adolescentes': forms.NumberInput(attrs={
                'class': 'w-20 px-3 py-2 border border-gray-300 rounded-lg text-center',
                'min': '0',
                'max': '10',
                'readonly': True,
            }),
            'nomes_adolescentes': forms.Textarea(attrs={  # Corrigido: era "nomes_adolescentes"
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Digite o nome de cada adolescente (um por linha)',
                'rows': 3
            }),
        }
        labels = {
            'nome': 'Nome *',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'qtd_adultos': 'Adultos',
            'nomes_adultos': 'Nome dos acompanhantes',
            'qtd_criancas': 'Crianças',
            'nomes_criancas': 'Nome das crianças',
            'qtd_adolescentes': 'Adolescentes/Crianças',
            'nomes_adolescentes': 'Nome dos adolescentes ou crianças',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields
        self.fields['nome'].required = True
        

    def clean(self):
        cleaned_data = super().clean()
        qtd_adultos = cleaned_data.get('qtd_adultos', 1)
        nomes_adultos = cleaned_data.get('nomes_adultos', '')
        qtd_criancas = cleaned_data.get('qtd_criancas', 0)
        nomes_criancas = cleaned_data.get('nomes_criancas', '')
        qtd_adolescentes = cleaned_data.get('qtd_adolescentes', 0)
        nomes_adolescentes = cleaned_data.get('nomes_adolescentes', '')

        # Validação para adultos (se mais de 1, nomes são obrigatórios)
        if qtd_adultos > 1 and not nomes_adultos.strip():
            self.add_error('nomes_adultos', 'Os nomes dos acompanhantes adultos são obrigatórios quando há mais de 1 adulto.')

        # Validação para crianças (se mais de 0, nomes são obrigatórios)
        if qtd_criancas > 0 and not nomes_criancas.strip():
            self.add_error('nomes_criancas', 'Os nomes das crianças são obrigatórios quando há crianças.')

        # Validação para adolescentes (se mais de 0, nomes são obrigatórios)
        if qtd_adolescentes > 0 and not nomes_adolescentes.strip():
            self.add_error('nomes_adolescentes', 'Os nomes dos adolescentes são obrigatórios quando há adolescentes.')

        # Validar se o número de nomes corresponde à quantidade
        if qtd_adultos > 1 and nomes_adultos.strip():
            nomes_lista = [nome.strip() for nome in nomes_adultos.split('\n') if nome.strip()]
            if len(nomes_lista) != qtd_adultos - 1:  # -1 porque o primeiro adulto é o próprio usuário
                self.add_error('nomes_adultos', f'Você deve informar {qtd_adultos - 1} nome(s) de acompanhante(s) adulto(s).')

        if qtd_criancas > 0 and nomes_criancas.strip():
            nomes_lista = [nome.strip() for nome in nomes_criancas.split('\n') if nome.strip()]
            if len(nomes_lista) != qtd_criancas:
                self.add_error('nomes_criancas', f'Você deve informar {qtd_criancas} nome(s) de criança(s).')

        # Adicionar validação para adolescentes
        if qtd_adolescentes > 0 and nomes_adolescentes.strip():
            nomes_lista = [nome.strip() for nome in nomes_adolescentes.split('\n') if nome.strip()]
            if len(nomes_lista) != qtd_adolescentes:
                self.add_error('nomes_adolescentes', f'Você deve informar {qtd_adolescentes} nome(s) de adolescente(s).')

        return cleaned_data


class CompraForm(forms.ModelForm):
    class Meta:
        model = CompraPresente
        fields = ['nome_comprador', 'email_comprador', 'telefone_comprador', 'mensagem']
        widgets = {
            'nome_comprador': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Seu nome completo *'
            }),
            'email_comprador': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'seu@email.com *'
            }),
            'telefone_comprador': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': '(81) 98888-8888 (opcional)'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-300 focus:border-transparent transition duration-200',
                'placeholder': 'Deixe uma mensagem carinhosa para nós... (opcional)',
                'rows': 4
            })
        }
        labels = {
            'nome_comprador': 'Nome Completo',
            'email_comprador': 'E-mail',
            'telefone_comprador': 'Telefone (opcional)',
            'mensagem': 'Mensagem para os Noivos (opcional)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone_comprador'].required = False
        self.fields['mensagem'].required = False
