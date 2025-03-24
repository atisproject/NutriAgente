import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from app import app, db
from models import Formulario, Lead, Interacao
from ai_agent import gerar_lembrete_formulario
from notification import enviar_sms, notificar_administrador, notificar_formulario_pendente

logger = logging.getLogger(__name__)

# Configuração do scheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
}
executors = {
    'default': ThreadPoolExecutor(20)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone='America/Sao_Paulo'
)

def verificar_formularios_pendentes():
    """
    Verifica formulários pendentes há mais de 2 dias e envia lembretes
    """
    try:
        logger.info("Iniciando verificação de formulários pendentes")
        
        data_limite = datetime.utcnow() - timedelta(days=2)
        formularios = Formulario.query.filter_by(
            status='pendente', 
            lembrete_enviado=False
        ).filter(
            Formulario.data_envio <= data_limite
        ).all()
        
        for formulario in formularios:
            try:
                lead = Lead.query.get(formulario.lead_id)
                if not lead:
                    continue
                
                # Gerar mensagem de lembrete personalizada
                mensagem = gerar_lembrete_formulario(lead.id, formulario.tipo)
                
                # Enviar SMS para o cliente
                envio_sucesso = enviar_sms(lead.telefone, mensagem)
                
                if envio_sucesso:
                    # Registrar a interação
                    nova_interacao = Interacao(
                        lead_id=lead.id,
                        mensagem=mensagem,
                        origem="sistema"
                    )
                    db.session.add(nova_interacao)
                    
                    # Atualizar o status do formulário
                    formulario.lembrete_enviado = True
                    db.session.commit()
                    
                    # Notificar administrador
                    dias_pendente = (datetime.utcnow() - formulario.data_envio).days
                    notificar_formulario_pendente(lead.nome, lead.telefone, formulario.tipo, dias_pendente)
                    
                    logger.info(f"Lembrete enviado para {lead.nome} sobre formulário {formulario.tipo}")
            
            except Exception as e:
                logger.error(f"Erro ao processar formulário {formulario.id}: {str(e)}")
                continue
        
        logger.info(f"Verificação concluída. {len(formularios)} formulários processados.")
        
    except Exception as e:
        logger.error(f"Erro ao verificar formulários pendentes: {str(e)}")

def verificar_leads_inativos():
    """
    Verifica leads inativos há mais de 5 dias e envia mensagem de reativação
    """
    try:
        logger.info("Iniciando verificação de leads inativos")
        
        data_limite = datetime.utcnow() - timedelta(days=5)
        
        # Busca leads com última interação antes da data limite
        leads_inativos = db.session.query(Lead).join(
            Interacao, Lead.id == Interacao.lead_id
        ).filter(
            Lead.status.in_(['novo', 'em_contato']),
            Interacao.data_hora <= data_limite
        ).group_by(Lead.id).all()
        
        for lead in leads_inativos:
            try:
                # Verificar se já tem uma interação de reativação recente
                interacao_recente = Interacao.query.filter_by(
                    lead_id=lead.id, 
                    origem="sistema"
                ).filter(
                    Interacao.data_hora >= (datetime.utcnow() - timedelta(days=3))
                ).first()
                
                if interacao_recente:
                    continue
                
                # Gerar mensagem de reativação
                mensagem = (
                    f"Olá {lead.nome}, sentimos sua falta! Gostaríamos de continuar "
                    f"ajudando você a alcançar seus objetivos nutricionais. "
                    f"Podemos esclarecer qualquer dúvida ou agendar uma consulta para você. "
                    f"Como podemos ajudar?"
                )
                
                # Enviar SMS
                envio_sucesso = enviar_sms(lead.telefone, mensagem)
                
                if envio_sucesso:
                    # Registrar a interação
                    nova_interacao = Interacao(
                        lead_id=lead.id,
                        mensagem=mensagem,
                        origem="sistema"
                    )
                    db.session.add(nova_interacao)
                    db.session.commit()
                    
                    logger.info(f"Mensagem de reativação enviada para {lead.nome}")
            
            except Exception as e:
                logger.error(f"Erro ao processar lead inativo {lead.id}: {str(e)}")
                continue
        
        logger.info(f"Verificação concluída. {len(leads_inativos)} leads inativos processados.")
        
    except Exception as e:
        logger.error(f"Erro ao verificar leads inativos: {str(e)}")

def iniciar_scheduler():
    """Inicia o agendador de tarefas"""
    scheduler.add_job(
        verificar_formularios_pendentes, 
        'interval', 
        hours=24, 
        id='verificar_formularios_pendentes'
    )
    
    scheduler.add_job(
        verificar_leads_inativos, 
        'interval', 
        hours=24, 
        id='verificar_leads_inativos'
    )
    
    scheduler.start()
    logger.info("Agendador de tarefas iniciado")

def parar_scheduler():
    """Para o agendador de tarefas"""
    scheduler.shutdown()
    logger.info("Agendador de tarefas parado")
