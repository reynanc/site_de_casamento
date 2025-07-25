import mercadopago

public_key = "APP_USR-2aaa4713-f2f2-4592-9fea-90f5eebb8069"
token = "APP_USR-4312193296075309-072001-ec0d15fafb531cb2599c799cb1c0d8a7-233685584"

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
        "notification_url": "https://www.laynan.com.br/webhook/mercadopago/",  # Substitua pelo seu domínio
    }
    
    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento