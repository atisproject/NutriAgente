import json
import os
import logging
from datetime import datetime
from openai import OpenAI
from flask import current_app
from models import Product, Lead, Conversation

# Configuração do cliente OpenAI
# o modelo mais recente da OpenAI é "gpt-4o" que foi lançado em 13 de maio de 2024.
# não altere isso a menos que explicitamente solicitado pelo usuário
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_welcome_message(custom_message=None):
    """Gera mensagem de boas-vindas personalizada"""
    if custom_message:
        return custom_message
    
    return """Olá! Sou o assistente virtual da Nutrição Saudável. 
    Estou aqui para ajudar você com suas dúvidas sobre nutrição e nossos serviços. 
    Como posso ajudar você hoje?"""

def get_product_info():
    """Retorna informações sobre produtos disponíveis"""
    products = Product.query.filter_by(is_active=True).all()
    product_info = []
    
    for product in products:
        product_info.append({
            "nome": product.name,
            "descricao": product.description,
            "preco": f"R$ {product.price:.2f}".replace('.', ',')
        })
    
    return product_info

def get_conversation_history(lead_id):
    """Recupera o histórico de conversa para contextualizar a IA"""
    # Limitando a 10 mensagens recentes para não exceder contexto
    history = Conversation.query.filter_by(lead_id=lead_id).order_by(
        Conversation.timestamp.desc()).limit(10).all()
    
    # Inverter para ordem cronológica
    history.reverse()
    
    formatted_history = []
    for msg in history:
        role = "assistant" if msg.is_bot else "user"
        formatted_history.append({"role": role, "content": msg.message})
    
    return formatted_history

def process_message(user_message, lead_id):
    """Processa mensagem do usuário usando OpenAI e retorna resposta"""
    try:
        # Atualizar informações de lead com base na mensagem
        update_lead_info(user_message, lead_id)
        
        # Obter histórico de conversa para contexto
        conversation_history = get_conversation_history(lead_id)
        
        # Obter informações de produtos
        product_info = get_product_info()
        
        # Criar prompt com sistema e histórico
        system_message = f"""Você é um assistente virtual especializado em nutrição da empresa 'Nutrição Saudável'.
        Seu objetivo é fornecer informações úteis sobre nutrição, esclarecer dúvidas e converter leads em clientes.
        
        Siga estas diretrizes:
        1. Seja amigável, profissional e empático
        2. Forneça informações precisas sobre nutrição e saúde
        3. Apresente os produtos/serviços da empresa quando apropriado
        4. Tente obter informações de contato como nome, e-mail e telefone
        5. Não invente informações sobre o cliente ou sobre nutrição
        6. Respostas devem ser em português do Brasil
        7. Mantenha respostas concisas (máximo 3 parágrafos)
        
        Produtos disponíveis:
        {json.dumps(product_info, ensure_ascii=False)}
        
        Se detectar intenção de compra, explique o processo: "Para adquirir este produto, preciso de seus dados para contato. Poderia me informar seu nome e telefone ou e-mail?"
        
        Se o cliente fornecer dados de contato, responda: "Obrigado! Em breve nossa equipe entrará em contato para finalizar seu atendimento."
        """
        
        messages = [{"role": "system", "content": system_message}]
        
        # Adicionar histórico de conversas
        messages.extend(conversation_history)
        
        # Adicionar mensagem atual do usuário se não estiver no histórico
        if not any(msg["role"] == "user" and msg["content"] == user_message for msg in conversation_history):
            messages.append({"role": "user", "content": user_message})
        
        # Fazer a chamada para a API da OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",  # o modelo mais recente da OpenAI é "gpt-4o"
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        return "Desculpe, tive um problema ao processar sua mensagem. Por favor, tente novamente."

def extract_contact_info(message):
    """Extrai informações de contato da mensagem do usuário"""
    try:
        prompt = f"""Extraia informações de contato da seguinte mensagem:
        "{message}"
        
        Retorne um JSON com os seguintes campos (deixe em branco se não encontrar):
        - name: nome completo da pessoa
        - email: endereço de e-mail
        - phone: número de telefone (apenas dígitos)
        
        Responda apenas com o JSON.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",  # o modelo mais recente da OpenAI é "gpt-4o"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logger.error(f"Erro ao extrair informações de contato: {e}")
        return {"name": "", "email": "", "phone": ""}

def update_lead_info(message, lead_id):
    """Atualiza informações do lead com base na mensagem"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return
        
        # Extrair informações de contato
        info = extract_contact_info(message)
        
        # Atualizar apenas campos vazios
        if info.get("name") and not lead.name:
            lead.name = info.get("name")
            
        if info.get("email") and not lead.email:
            lead.email = info.get("email")
            
        if info.get("phone") and not lead.phone:
            lead.phone = info.get("phone")
        
        # Detectar intenção de compra
        if is_purchase_intent(message) and lead.status != "convertido":
            lead.status = "convertido"
        
        from app import db
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Erro ao atualizar informações do lead: {e}")

def is_purchase_intent(message):
    """Verifica se a mensagem indica intenção de compra"""
    try:
        prompt = f"""Analise a seguinte mensagem e determine se há uma intenção clara de compra ou contratação de serviço:
        "{message}"
        
        Responda apenas com um JSON no formato: {{"is_purchase_intent": true/false}}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",  # o modelo mais recente da OpenAI é "gpt-4o"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("is_purchase_intent", False)
        
    except Exception as e:
        logger.error(f"Erro ao verificar intenção de compra: {e}")
        return False
