// Gerenciamento do chat em tempo real

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do chat
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Armazenamento da sessão
    let sessionId = localStorage.getItem('chat_session_id') || '';
    
    // Rolagem automática para o final do chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Adicionar mensagem ao chat
    function addMessage(text, isBot = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isBot ? 'message-bot' : 'message-user');
        messageElement.textContent = text;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Enviar mensagem para o servidor
    function sendMessage(message) {
        // Mostrar indicador de carregamento
        loadingIndicator.style.display = 'inline-block';
        sendButton.disabled = true;
        
        // Preparar dados para envio
        const data = {
            message: message,
            session_id: sessionId
        };
        
        // Fazer requisição para a API
        fetch('/api/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Esconder indicador de carregamento
            loadingIndicator.style.display = 'none';
            sendButton.disabled = false;
            
            // Adicionar resposta do bot
            addMessage(data.message, true);
            
            // Armazenar ID de sessão se recebido
            if (data.session_id && !sessionId) {
                sessionId = data.session_id;
                localStorage.setItem('chat_session_id', sessionId);
            }
        })
        .catch(error => {
            console.error('Erro ao enviar mensagem:', error);
            loadingIndicator.style.display = 'none';
            sendButton.disabled = false;
            
            // Mensagem de erro
            addMessage('Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.', true);
        });
    }
    
    // Manipulador de evento para envio de mensagem
    function handleSendMessage() {
        const message = messageInput.value.trim();
        
        if (message) {
            // Adicionar mensagem do usuário
            addMessage(message);
            
            // Limpar campo de input
            messageInput.value = '';
            
            // Enviar para o servidor
            sendMessage(message);
        }
    }
    
    // Evento de clique no botão de enviar
    sendButton.addEventListener('click', handleSendMessage);
    
    // Evento de tecla Enter no input
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
    
    // Se não houver sessão, enviar mensagem vazia para obter mensagem de boas-vindas
    if (!sessionId) {
        sendMessage('');
    }
});
