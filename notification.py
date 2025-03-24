import os
import logging
from twilio.rest import Client
from app import app

# Configuração do Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
ADMIN_PHONE_NUMBER = "61985870944"  # Número específico para notificações

logger = logging.getLogger(__name__)

def enviar_sms(numero_destino, mensagem):
    """
    Envia uma mensagem SMS utilizando a API do Twilio
    
    Args:
        numero_destino (str): Número de telefone de destino
        mensagem (str): Conteúdo da mensagem a ser enviada
    
    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário
    """
    try:
        # Verificar se as credenciais da Twilio estão configuradas
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
            logger.error("Credenciais da Twilio não configuradas")
            return False
        
        # Inicializar o cliente Twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Certificar que o número de telefone está no formato internacional
        if not numero_destino.startswith('+'):
            # Formato brasileiro (+55)
            if numero_destino.startswith('0'):
                numero_destino = '+55' + numero_destino[1:]
            else:
                numero_destino = '+55' + numero_destino
        
        # Enviar a mensagem
        message = client.messages.create(
            body=mensagem,
            from_=TWILIO_PHONE_NUMBER,
            to=numero_destino
        )
        
        logger.info(f"Mensagem enviada com sucesso. SID: {message.sid}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar SMS: {str(e)}")
        return False

def notificar_administrador(assunto, conteudo):
    """
    Envia uma notificação para o número do administrador
    
    Args:
        assunto (str): Assunto da notificação
        conteudo (str): Conteúdo detalhado da notificação
    
    Returns:
        bool: True se a notificação foi enviada com sucesso, False caso contrário
    """
    mensagem = f"NutriAI - {assunto}\n\n{conteudo}"
    return enviar_sms(ADMIN_PHONE_NUMBER, mensagem)

def notificar_novo_lead(nome, telefone):
    """
    Notifica o administrador sobre um novo lead
    
    Args:
        nome (str): Nome do lead
        telefone (str): Telefone do lead
    
    Returns:
        bool: True se a notificação foi enviada com sucesso, False caso contrário
    """
    mensagem = f"Novo lead registrado!\nNome: {nome}\nTelefone: {telefone}"
    return notificar_administrador("Novo Lead", mensagem)

def notificar_formulario_pendente(nome, telefone, tipo_formulario, dias_pendente):
    """
    Notifica o administrador sobre formulários pendentes por muito tempo
    
    Args:
        nome (str): Nome do cliente
        telefone (str): Telefone do cliente
        tipo_formulario (str): Tipo do formulário pendente
        dias_pendente (int): Quantidade de dias pendente
    
    Returns:
        bool: True se a notificação foi enviada com sucesso, False caso contrário
    """
    mensagem = f"Formulário pendente há {dias_pendente} dias!\nCliente: {nome}\nTelefone: {telefone}\nFormulário: {tipo_formulario}"
    return notificar_administrador("Formulário Pendente", mensagem)

def notificar_potencial_conversao(nome, telefone, probabilidade):
    """
    Notifica o administrador sobre um lead com alta probabilidade de conversão
    
    Args:
        nome (str): Nome do lead
        telefone (str): Telefone do lead
        probabilidade (float): Probabilidade de conversão (0-1)
    
    Returns:
        bool: True se a notificação foi enviada com sucesso, False caso contrário
    """
    prob_percentual = int(probabilidade * 100)
    mensagem = f"Lead com alta probabilidade de conversão ({prob_percentual}%)!\nNome: {nome}\nTelefone: {telefone}"
    return notificar_administrador("Oportunidade de Conversão", mensagem)
