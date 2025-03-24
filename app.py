import os
import logging
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash


# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Classe base para SQLAlchemy
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Criação da aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///nutricao.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o app com a extensão
db.init_app(app)

# Importação circular evitada com importação dentro do contexto da aplicação
with app.app_context():
    from models import User, Lead, Conversation, Product, FormConfig
    from services.ai_agent import process_message, generate_welcome_message
    from services.twilio_service import send_notification
    from services.scheduler import check_pending_forms
    
    db.create_all()
    
    # Criar produtos e configurações padrão se não existirem
    if not Product.query.first():
        produtos_iniciais = [
            Product(name="Consulta Nutricional", description="Consulta completa com análise personalizada", price=150.00),
            Product(name="Plano Alimentar Básico", description="Plano alimentar para 30 dias", price=120.00),
            Product(name="Plano Alimentar Premium", description="Plano alimentar personalizado com acompanhamento", price=250.00),
            Product(name="Suplemento Proteico", description="Suplemento proteico de alta qualidade", price=89.90)
        ]
        db.session.add_all(produtos_iniciais)
        
    if not FormConfig.query.first():
        config_padrao = FormConfig(
            welcome_message="Olá! Sou o assistente virtual da Nutrição Saudável. Como posso ajudar você hoje?",
            follow_up_hours=24,
            notification_number="61985870944"
        )
        db.session.add(config_padrao)
    
    db.session.commit()


@app.route('/')
def index():
    """Rota principal que exibe o chat para o cliente"""
    return render_template('index.html')


@app.route('/api/message', methods=['POST'])
def receive_message():
    """Endpoint para receber mensagens do chat"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', '')
    
    # Gerar ou recuperar um ID de sessão para o lead
    if not session_id:
        session_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(hash(request.remote_addr))[:5]
        
    # Verificar se esse lead já existe
    lead = Lead.query.filter_by(session_id=session_id).first()
    if not lead:
        # Criar um novo lead
        lead = Lead(
            session_id=session_id,
            source="website_chat",
            status="novo"
        )
        db.session.add(lead)
        db.session.commit()
        
        # Mensagem de boas-vindas
        config = FormConfig.query.first()
        welcome_message = generate_welcome_message(config.welcome_message if config else None)
        
        # Salvar conversa no banco
        conversation = Conversation(
            lead_id=lead.id,
            message=welcome_message,
            is_bot=True,
            timestamp=datetime.now()
        )
        db.session.add(conversation)
        db.session.commit()
        
        # Enviar notificação de novo lead
        try:
            send_notification(
                f"Novo lead iniciou conversa. ID: {lead.id}",
                config.notification_number if config else "61985870944"
            )
        except Exception as e:
            logging.error(f"Erro ao enviar notificação: {e}")
        
        return jsonify({
            'message': welcome_message,
            'session_id': session_id
        })
    
    # Salvar mensagem do usuário
    user_conversation = Conversation(
        lead_id=lead.id,
        message=user_message,
        is_bot=False,
        timestamp=datetime.now()
    )
    db.session.add(user_conversation)
    db.session.commit()
    
    # Processar mensagem com IA
    ai_response = process_message(user_message, lead.id)
    
    # Salvar resposta da IA
    bot_conversation = Conversation(
        lead_id=lead.id,
        message=ai_response,
        is_bot=True,
        timestamp=datetime.now()
    )
    db.session.add(bot_conversation)
    
    # Atualizar status do lead
    lead.last_interaction = datetime.now()
    if lead.status == "novo":
        lead.status = "em_conversa"
        
    db.session.commit()
    
    return jsonify({
        'message': ai_response,
        'session_id': session_id
    })


@app.route('/dashboard')
def dashboard():
    """Dashboard administrativo"""
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    
    # Estatísticas básicas
    total_leads = Lead.query.count()
    leads_convertidos = Lead.query.filter_by(status="convertido").count()
    taxa_conversao = (leads_convertidos / total_leads * 100) if total_leads > 0 else 0
    
    return render_template(
        'dashboard.html',
        leads=leads,
        total_leads=total_leads,
        leads_convertidos=leads_convertidos,
        taxa_conversao=round(taxa_conversao, 2)
    )


@app.route('/config', methods=['GET', 'POST'])
def config():
    """Configuração do agente de IA"""
    if request.method == 'POST':
        config = FormConfig.query.first()
        if not config:
            config = FormConfig()
            
        config.welcome_message = request.form.get('welcome_message')
        config.follow_up_hours = int(request.form.get('follow_up_hours'))
        config.notification_number = request.form.get('notification_number')
        
        db.session.add(config)
        db.session.commit()
        
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('config'))
    
    config = FormConfig.query.first()
    products = Product.query.all()
    return render_template('config.html', config=config, products=products)


@app.route('/products', methods=['POST'])
def save_product():
    """Salvar ou atualizar produto"""
    product_id = request.form.get('product_id')
    
    if product_id and product_id.isdigit():
        # Atualizar produto existente
        product = Product.query.get(int(product_id))
        if product:
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price'))
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
    else:
        # Criar novo produto
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price'))
        )
        db.session.add(product)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
    
    return redirect(url_for('config'))


@app.route('/lead/<int:lead_id>')
def view_lead(lead_id):
    """Visualizar detalhes de um lead"""
    lead = Lead.query.get_or_404(lead_id)
    conversations = Conversation.query.filter_by(lead_id=lead_id).order_by(Conversation.timestamp).all()
    
    return render_template('lead_detail.html', lead=lead, conversations=conversations)


@app.route('/api/lead/<int:lead_id>/convert', methods=['POST'])
def convert_lead(lead_id):
    """Marcar lead como convertido"""
    lead = Lead.query.get_or_404(lead_id)
    lead.status = "convertido"
    db.session.commit()
    
    # Enviar notificação
    config = FormConfig.query.first()
    try:
        send_notification(
            f"Lead #{lead_id} foi convertido com sucesso!",
            config.notification_number if config else "61985870944"
        )
    except Exception as e:
        logging.error(f"Erro ao enviar notificação: {e}")
    
    return jsonify({"success": True})


@app.route('/api/statistics')
def get_statistics():
    """Endpoint para obter estatísticas para o dashboard"""
    # Total de leads nos últimos 30 dias por dia
    from sqlalchemy import func
    import datetime
    
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    
    # Leads por dia
    leads_by_day = db.session.query(
        func.date(Lead.created_at).label('date'),
        func.count().label('count')
    ).filter(Lead.created_at >= thirty_days_ago).group_by(func.date(Lead.created_at)).all()
    
    # Conversões por dia
    conversions_by_day = db.session.query(
        func.date(Lead.created_at).label('date'),
        func.count().label('count')
    ).filter(Lead.created_at >= thirty_days_ago, Lead.status == 'convertido').group_by(func.date(Lead.created_at)).all()
    
    # Preparar dados para o formato necessário para gráficos
    dates = [result.date.strftime('%Y-%m-%d') for result in leads_by_day]
    leads_counts = [result.count for result in leads_by_day]
    
    conversion_dates = {result.date.strftime('%Y-%m-%d'): result.count for result in conversions_by_day}
    conversion_counts = [conversion_dates.get(date, 0) for date in dates]
    
    return jsonify({
        "dates": dates,
        "leads": leads_counts,
        "conversions": conversion_counts
    })


@app.route('/schedule_check')
def manual_check():
    """Verificar manualmente formulários pendentes"""
    count = check_pending_forms()
    return jsonify({"message": f"{count} formulários pendentes processados"})


# Verificação periódica de formulários pendentes (executada na primeira requisição)
@app.before_first_request
def setup_scheduler():
    import threading
    import time
    
    def run_scheduler():
        while True:
            with app.app_context():
                try:
                    check_pending_forms()
                except Exception as e:
                    logging.error(f"Erro ao verificar formulários pendentes: {e}")
            # Verificar a cada 1 hora
            time.sleep(3600)
    
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
