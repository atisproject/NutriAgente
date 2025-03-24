import os
import logging
from twilio.rest import Client

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configurações do Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_notification(message, to_number):
    """
    Envia notificação via SMS usando Twilio
    
    Args:
        message: Texto da mensagem a ser enviada
        to_number: Número de telefone do destinatário
    
    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    try:
        # Garantir que o número está no formato correto
        if not to_number.startswith("+"):
            # Adicionar código do Brasil se necessário
            if to_number.startswith("0"):
                to_number = "+55" + to_number[1:]
            else:
                to_number = "+55" + to_number
        
        # Formatar como E.164 - remover caracteres não numéricos
        formatted_number = ''.join(char for char in to_number if char.isdigit() or char == '+')
        
        # Inicializar cliente Twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Enviar a mensagem
        message_sent = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_number
        )
        
        logger.info(f"Mensagem enviada com SID: {message_sent.sid}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {e}")
        return False

def send_lead_notification(lead_info):
    """
    Envia notificação sobre um novo lead ou lead atualizado
    
    Args:
        lead_info: Dicionário com informações do lead
    """
    from models import FormConfig
    
    try:
        config = FormConfig.query.first()
        notification_number = config.notification_number if config else "61985870944"
        
        # Montar mensagem
        message = f"""
Nutrição Saudável - Novo Lead
ID: {lead_info.get('id', 'N/A')}
Nome: {lead_info.get('name', 'Não informado')}
Email: {lead_info.get('email', 'Não informado')}
Telefone: {lead_info.get('phone', 'Não informado')}
Status: {lead_info.get('status', 'Novo')}
"""
        
        # Enviar notificação
        send_notification(message, notification_number)
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação de lead: {e}")
