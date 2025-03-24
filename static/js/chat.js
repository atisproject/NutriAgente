// Chat.js - Funcionalidades para a interface de chat

document.addEventListener('DOMContentLoaded', function() {
    initChatInterface();
});

/**
 * Inicializa a interface de chat e seus eventos
 */
function initChatInterface() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.querySelector('.chat-container');
    
    if (!chatForm || !chatInput || !chatContainer) return;

    // Rola o chat para a última mensagem
    scrollToBottom(chatContainer);

    // Evento de submissão do formulário
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const mensagem = chatInput.value.trim();
        if (!mensagem) return;
        
        // Desabilita o input e botão enquanto envia
        chatInput.disabled = true;
        sendButton.disabled = true;
        
        // Adiciona a mensagem do usuário ao chat
        adicionarMensagemChat('usuario', mensagem);
        chatInput.value = '';
        
        // Adiciona indicador de digitação
        const typingIndicator = adicionarIndicadorDigitacao();
        
        // Obtém o ID do lead da URL
        const leadId = document.getElementById('lead-id').value;
        
        // Envia a mensagem para o backend
        enviarMensagem(leadId, mensagem)
            .then(response => {
                // Remove o indicador de digitação
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                
                // Adiciona a resposta do agente ao chat
                if (response && response.resposta) {
                    adicionarMensagemChat('ia', response.resposta);
                } else {
                    mostrarErroChat('Não foi possível processar sua mensagem. Tente novamente.');
                }
            })
            .catch(error => {
                console.error('Erro ao enviar mensagem:', error);
                // Remove o indicador de digitação
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                mostrarErroChat('Erro ao enviar mensagem. Verifique sua conexão e tente novamente.');
            })
            .finally(() => {
                // Reabilita o input e botão
                chatInput.disabled = false;
                sendButton.disabled = false;
                chatInput.focus();
            });
    });
    
    // Evento de tecla Enter para enviar mensagem
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendButton.click();
        }
    });
}

/**
 * Adiciona uma nova mensagem ao chat
 * @param {string} tipo - Tipo de mensagem ('usuario', 'ia', 'sistema')
 * @param {string} texto - Texto da mensagem
 */
function adicionarMensagemChat(tipo, texto) {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return;
    
    const mensagemElement = document.createElement('div');
    mensagemElement.className = `chat-message ${tipo}`;
    
    // Adiciona ícone conforme o tipo de mensagem
    let icone = '';
    if (tipo === 'usuario') {
        icone = '<i class="fas fa-user me-2"></i>';
    } else if (tipo === 'ia') {
        icone = '<i class="fas fa-robot me-2"></i>';
    } else {
        icone = '<i class="fas fa-cog me-2"></i>';
    }
    
    // Formata a data atual
    const agora = new Date();
    const dataFormatada = agora.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    // Formata links no texto
    const textoFormatado = formatarLinksNoTexto(texto);
    
    // Monta o HTML da mensagem
    mensagemElement.innerHTML = `
        <div>${icone}${textoFormatado}</div>
        <span class="chat-message-time">${dataFormatada}</span>
    `;
    
    chatContainer.appendChild(mensagemElement);
    scrollToBottom(chatContainer);
}

/**
 * Adiciona um indicador de "digitando..." ao chat
 * @returns {HTMLElement} Elemento do indicador adicionado
 */
function adicionarIndicadorDigitacao() {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return null;
    
    const indicadorElement = document.createElement('div');
    indicadorElement.className = 'chat-message ia typing-indicator';
    indicadorElement.innerHTML = `
        <div>
            <i class="fas fa-robot me-2"></i>
            <span class="typing-animation">Digitando<span>.</span><span>.</span><span>.</span></span>
        </div>
    `;
    
    chatContainer.appendChild(indicadorElement);
    scrollToBottom(chatContainer);
    
    return indicadorElement;
}

/**
 * Mostra uma mensagem de erro no chat
 * @param {string} mensagem - Mensagem de erro
 */
function mostrarErroChat(mensagem) {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return;
    
    const errorElement = document.createElement('div');
    errorElement.className = 'chat-message sistema';
    errorElement.innerHTML = `
        <div><i class="fas fa-exclamation-circle me-2"></i>${mensagem}</div>
        <span class="chat-message-time">${new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}</span>
    `;
    
    chatContainer.appendChild(errorElement);
    scrollToBottom(chatContainer);
    
    // Remove a mensagem de erro após 10 segundos
    setTimeout(() => {
        errorElement.style.opacity = '0';
        setTimeout(() => {
            if (errorElement.parentNode === chatContainer) {
                chatContainer.removeChild(errorElement);
            }
        }, 500);
    }, 10000);
}

/**
 * Formata links de texto para que sejam clicáveis
 * @param {string} texto - Texto para formatar
 * @returns {string} Texto formatado com links clicáveis
 */
function formatarLinksNoTexto(texto) {
    // Regex para identificar URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    
    // Substitui URLs por links clicáveis
    return texto.replace(urlRegex, url => {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });
}

/**
 * Envia uma mensagem para o backend
 * @param {string} leadId - ID do lead
 * @param {string} mensagem - Texto da mensagem
 * @returns {Promise} Promessa com a resposta
 */
function enviarMensagem(leadId, mensagem) {
    return fetch('/api/enviar_mensagem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            lead_id: leadId,
            mensagem: mensagem
        }),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.status);
        }
        return response.json();
    });
}

/**
 * Rola o container de chat para a última mensagem
 * @param {HTMLElement} container - Container de chat
 */
function scrollToBottom(container) {
    if (!container) return;
    container.scrollTop = container.scrollHeight;
}
