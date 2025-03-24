from flask import request, jsonify, flash, redirect, url_for
from app import app, db
from twilio.twiml.messaging_response import MessagingResponse
from whatsapp_integration import processar_mensagem_whatsapp, enviar_mensagem_whatsapp
from models import Lead, Interacao, Formulario
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook para receber mensagens do WhatsApp via Twilio
    
    Essa rota recebe as notificações da Twilio quando uma nova mensagem é enviada
    para o número do WhatsApp. A mensagem é processada e uma resposta é enviada.
    """
    try:
        # Obter os parâmetros do formulário
        mensagem_de = request.values.get('From', '')
        mensagem_texto = request.values.get('Body', '')
        
        logger.info(f"Mensagem WhatsApp recebida de {mensagem_de}: {mensagem_texto}")
        
        # Processar a mensagem se não estiver vazia
        if mensagem_texto.strip():
            # Processar a mensagem e obter a resposta
            resposta = processar_mensagem_whatsapp(mensagem_de, mensagem_texto)
            
            # Criar resposta TwiML
            resp = MessagingResponse()
            resp.message(resposta)
            
            return str(resp)
        
        return 'OK'
    except Exception as e:
        logger.error(f"Erro no webhook do WhatsApp: {str(e)}")
        return 'Erro no processamento da mensagem', 500

@app.route('/api/whatsapp/enviar', methods=['POST'])
def enviar_whatsapp():
    """
    API para enviar mensagens do WhatsApp manualmente
    
    Esta rota permite que os administradores do sistema enviem mensagens
    para os clientes via WhatsApp a partir da interface web.
    """
    try:
        # Requisição deve ser JSON
        dados = request.get_json()
        
        if not dados:
            return jsonify({'status': 'erro', 'mensagem': 'Dados não fornecidos'}), 400
        
        lead_id = dados.get('lead_id')
        mensagem = dados.get('mensagem')
        
        if not lead_id or not mensagem:
            return jsonify({'status': 'erro', 'mensagem': 'ID do lead e mensagem são obrigatórios'}), 400
        
        # Buscar o lead
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({'status': 'erro', 'mensagem': 'Lead não encontrado'}), 404
        
        # Enviar mensagem via WhatsApp
        enviado = enviar_mensagem_whatsapp(lead.telefone, mensagem)
        
        if enviado:
            # Registrar a interação
            nova_interacao = Interacao(
                lead_id=lead_id,
                mensagem=mensagem,
                origem='sistema'  # Ou 'usuario' se preferir
            )
            db.session.add(nova_interacao)
            db.session.commit()
            
            return jsonify({
                'status': 'sucesso',
                'mensagem': 'Mensagem enviada com sucesso'
            })
        else:
            return jsonify({
                'status': 'erro',
                'mensagem': 'Falha ao enviar mensagem via WhatsApp'
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem WhatsApp: {str(e)}")
        return jsonify({
            'status': 'erro',
            'mensagem': f'Erro ao processar solicitação: {str(e)}'
        }), 500

@app.route('/whatsapp/configuracao', methods=['GET', 'POST'])
def whatsapp_configuracao():
    """
    Página para configuração do WhatsApp
    
    Esta rota permite configurar as mensagens padrões e outras
    configurações relacionadas ao WhatsApp.
    """
    if request.method == 'POST':
        # Processar o formulário de configuração
        # Aqui você pode salvar configurações específicas do WhatsApp
        flash('Configurações do WhatsApp atualizadas com sucesso', 'success')
        return redirect(url_for('configuracoes'))
    
    # Esta rota seria acessível a partir da página de configurações
    return redirect(url_for('configuracoes'))