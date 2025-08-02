# Vamos salvar o conteúdo do README final no arquivo README.md existente

readme_content = """
# 💍 Site de Casamento - Laiane & Reynan 💜

Um site completo para casamento desenvolvido em **Django**, com sistema de confirmação de presença, lista de presentes com pagamentos via **MercadoPago** e envio automático de emails de agradecimento.

---

## 📋 Funcionalidades Principais

### 🏠 Página Inicial (Home)
- Design elegante e responsivo
- Contador de visitantes em tempo real
- Navegação intuitiva para todas as seções

### 💌 Sistema de Mensagens
- Formulário para convidados enviarem mensagens aos noivos
- Armazenamento seguro no banco de dados
- Interface administrativa para visualização

### ✅ Confirmação de Presença
- Formulário completo para confirmação de presença
- Campos para adultos, crianças e adolescentes
- Validação de dados e feedback ao usuário
- Armazenamento de informações de contato

### 🎁 Lista de Presentes
- **Catálogo Completo:** Presentes organizados por categorias (Casa, Sala, Cozinha, Quarto, Banheiro, Decoração, Eletrônicos, Outros)
- **Sistema de Filtros:** Filtrar por categoria e ordenar por preço
- **Controle de Estoque:** Quantidade disponível e status de esgotado
- **Imagens e Descrições:** Upload de imagens e descrições detalhadas
- **Links Externos:** Links para visualizar produtos em lojas

### 💳 Sistema de Pagamentos (MercadoPago)
- Integração completa com a API do MercadoPago
- Múltiplas formas de pagamento: cartão, PIX, boleto
- Webhooks para atualização automática de status de pagamento
- URLs de retorno e controle completo de transações

### 📧 Sistema de Email Automático
- Envio de emails de agradecimento automático após pagamento aprovado
- Template HTML estilizado
- Integração com Gmail via SMTP seguro

### 📊 Painel Administrativo
- Gestão de presentes, compras, mensagens e confirmações de presença
- Relatórios de visitantes e transações

---

## 🛠️ Tecnologias Utilizadas

**Backend**
- Django 5.2.4
- Python 3.x
- SQLite (desenvolvimento) / PostgreSQL (produção)
- MercadoPago SDK
- python-decouple (variáveis de ambiente)

**Frontend**
- HTML5 / CSS3
- TailwindCSS
- JavaScript
- Design responsivo

**Integrações**
- MercadoPago API (pagamentos)
- Gmail SMTP (envio de emails)
- Pillow (processamento de imagens)

---

## 📁 Estrutura do Projeto

site_de_casamento/
├── Casamento/ # Configurações do Django
│ ├── settings.py # Configurações principais
│ ├── urls.py # URLs principais
│ └── wsgi.py # Configuração WSGI
├── app_casamento/ # Aplicação principal
│ ├── models.py # Modelos de dados
│ ├── views.py # Lógica das views
│ ├── forms.py # Formulários
│ ├── admin.py # Configuração do admin
│ ├── api_mercado_pago.py # Integração MercadoPago
│ ├── middleware.py # Middleware personalizado
│ └── templates/ # Templates HTML
├── static/ # Arquivos estáticos (CSS, JS, imagens)
├── media/ # Uploads de usuários
├── templates/ # Templates base
└── requirements.txt # Dependências


---

## 🚀 Configuração e Instalação

### 1. Clonar o Repositório 
```bash
git clone <url-do-repositorio>
cd site_de_casamento
```
### 2. Criar Ambiente Virtual
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
source venv/bin/activate  # Linux/Mac
```
### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```
### 4. Configurar Variáveis de Ambiente
```bash
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
MERCADOPAGO_ACCESS_TOKEN=seu_access_token
MERCADOPAGO_PUBLIC_KEY=sua_public_key
```
### 5. Executar o Projeto
```bash
python manage.py migrate
python manage.py runserver
```
### 6. Criar Superusuário
```bash
python manage.py createsuperuser
```
### 7. Executar o Servidor
```bash
python manage.py runserver
```
## 🔧 Configurações Importantes

### Email (Gmail)
1. Ativar verificação em duas etapas
2. Criar uma senha de app
3. Configurar no arquivo .env

### MercadoPago
1. Criar conta de desenvolvedor
2. Obter credenciais de teste/produção
3. Configurar webhook:
https://seudominio.com/webhook/mercadopago/

### Segurança
- Todas as credenciais devem estar em variáveis de ambiente
- .env adicionado ao .gitignore
- DEBUG=False em produção
- ALLOWED_HOSTS configurado adequadamente

## 📱 Funcionalidades por Página
- **Home (/) → Apresentação dos noivos, data do casamento e navegação principal**
- **Cerimônia e Espaço (/cerimonia-espaco/) → Informações sobre local e horário**
- **Confirmar Presença (/confirmar-presenca/) → Formulário de confirmação de presença**
- **Lista de Presentes (/lista-presentes/) → Catálogo de presentes e sistema de compra**
- **Mensagens (/mensagens/) → Envio de mensagens aos noivos**
- **Admin (/admin/) → Gerenciamento completo e relatórios**

## 🐛 Debug e Monitoramento
- Logs de email
- Logs de pagamentos
- Logs de erros de aplicação

### Comandos Úteis
```bash
python manage.py check
python manage.py collectstatic
python manage.py test
python manage.py shell
```

## 🚀 Deploy em Produção
- DEBUG=False
- Configuração de ALLOWED_HOSTS
- Banco SQLite
- Coleta de arquivos estáticos

### Plataforma de uso:
- AWS

## 📈 Estatísticas e Monitoramento
- Contador de visitantes em tempo real
- Relatórios de compras via Django Admin
- Logs de email e status de pagamentos

## 🔒 Segurança Implementada
- Proteção CSRF
- Validação de formulários
- Sanitização de dados
- Credenciais em variáveis de ambiente
- Middleware de segurança

## 📞 Suporte e Manutenção
- Logs detalhados
- Backup regular do banco de dados
- Versionamento de código

## Desenvolvido por:
- Reynan
- Data do Casamento: 13/12/2025 

## 📝 Notas de Desenvolvimento
Projeto completo com confirmação de presença, lista de presentes com pagamento integrado, envio automático de emails e painel administrativo robusto.
Pronto para produção e seguro.





