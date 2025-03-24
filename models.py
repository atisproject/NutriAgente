from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Modelo para usuários administrativos"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Lead(db.Model):
    """Modelo para leads/clientes potenciais"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    session_id = db.Column(db.String(50), unique=True)
    source = db.Column(db.String(50))  # website, formulário, etc.
    status = db.Column(db.String(20))  # novo, em_conversa, convertido, abandonado
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_interaction = db.Column(db.DateTime, default=datetime.now)
    
    conversations = db.relationship('Conversation', backref='lead', lazy=True)
    
    def __repr__(self):
        return f'<Lead {self.id} - {self.name or "Sem nome"}>'


class Conversation(db.Model):
    """Histórico de conversas com os leads"""
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_bot = db.Column(db.Boolean, default=False)  # True se mensagem do bot, False se do cliente
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Conversation {self.id} - Lead {self.lead_id}>'


class Product(db.Model):
    """Produtos de nutrição disponíveis para venda"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class FormConfig(db.Model):
    """Configurações para o agente de IA e formulários"""
    id = db.Column(db.Integer, primary_key=True)
    welcome_message = db.Column(db.Text)
    follow_up_hours = db.Column(db.Integer, default=24)  # Intervalo em horas para acompanhamento
    notification_number = db.Column(db.String(20))  # Número para envio de notificações
    
    def __repr__(self):
        return f'<FormConfig {self.id}>'
