import logging
from datetime import datetime, timedelta
from models import Lead, FormConfig
from services.twilio_service import send_notification

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_pending_forms():
    """
    Verifica leads que não responderam ou não completaram o formulário
    e envia mensagem de acompanhamento
    
    Returns:
        int: Número de leads processados
    """
    try:
        from app import db
        
        # Obter configuração
        config = FormConfig.query.first()
        follow_up_hours = config.follow_up_hours if config else 24
        notification_number = config.notification_number if config else "61985870944"
        
        # Calcular limite de tempo para acompanhamento
        time_threshold = datetime.now() - timedelta(hours=follow_up_hours)
        
        # Buscar leads inativos ou incompletos
        pending_leads = Lead.query.filter(
            (Lead.status.in_(["novo", "em_conversa"])) &
            (Lead.last_interaction < time_threshold)
        ).all()
        
        count = 0
        for lead in pending_leads:
            # Verificar se tem informações suficientes para contato
            if lead.email or lead.phone:
                # Criar mensagem personalizada com as informações disponíveis
                message = _generate_follow_up_message(lead)
                
                # Enviar mensagem se tiver telefone
                if lead.phone:
                    send_notification(message, lead.phone)
                
                # Atualizar status do lead
                lead.status = "aguardando_resposta"
                lead.last_interaction = datetime.now()
                count += 1
            
            # Independente se enviou ou não, notificar administrador
            admin_message = f"Lead #{lead.id} ({lead.name or 'Sem nome'}) está inativo há mais de {follow_up_hours} horas."
            send_notification(admin_message, notification_number)
        
        db.session.commit()
        logger.info(f"Processados {count} leads pendentes")
        return count
        
    except Exception as e:
        logger.error(f"Erro ao verificar formulários pendentes: {e}")
        return 0

def _generate_follow_up_message(lead):
    """
    Gera mensagem personalizada de acompanhamento
    
    Args:
        lead: Objeto Lead com informações do cliente
    
    Returns:
        str: Mensagem personalizada
    """
    if lead.name:
        greeting = f"Olá {lead.name.split()[0]}!"
    else:
        greeting = "Olá!"
    
    message = f"""{greeting}

Notamos que você iniciou uma conversa com nossa equipe de nutrição, mas não finalizou o atendimento.

A Nutrição Saudável está à disposição para ajudá-lo a alcançar seus objetivos de saúde e bem-estar.

Podemos continuar nossa conversa? Estamos disponíveis para esclarecer qualquer dúvida sobre nossos serviços.

Atenciosamente,
Equipe Nutrição Saudável
"""
    
    return message
