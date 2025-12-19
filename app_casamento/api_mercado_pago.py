import mercadopago

public_key = "SUA_PUBLIC_KEY"
token = "SEU_TOKEN"

def criar_pagamento_presente(presente, link_retorno, compra_id):
    """Função específica para pagamento de presentes de casamento"""
    sdk = mercadopago.SDK(token)
    
    preference_data = {
        "items": [{
            "title": f"Presente de Casamento: {presente.nome}",
            "quantity": 1,
            "unit_price": float(presente.preco),
        }],
        "back_urls": {
            "success": link_retorno,
            "pending": link_retorno,
            "failure": link_retorno,
        },
        "external_reference": str(compra_id),  # Importante para o webhook
        "notification_url": "https://seudominio.com/webhook/mercadopago/",  # Substitua pelo seu domínio
    }
    
    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento