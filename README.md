# NutriAI - Sistema Inteligente de Nutrição

## Descrição

NutriAI é um sistema automatizado com inteligência artificial para conversão de leads e atendimento ao cliente para empresas de nutrição. O sistema utiliza IA para personalizar conversas, esclarecer dúvidas e vender produtos automaticamente.

## Principais Funcionalidades

- **Agente de IA Comercial**: Opera 24/7, personalizando conversas e esclarecendo dúvidas
- **Comunicação Multicanal**: Integração com SMS e WhatsApp
- **Acompanhamento de Leads**: Sistema inteligente de gestão e acompanhamento de leads
- **Lembretes Automáticos**: Envio de lembretes para formulários não respondidos
- **Base de Conhecimento**: Sistema central para gerenciar informações sobre produtos e serviços
- **Dashboard Administrativo**: Interface completa para gerenciamento de leads e configurações

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite/PostgreSQL
- **IA**: OpenAI API (GPT-4)
- **Comunicação**: Twilio API (SMS e WhatsApp)
- **Frontend**: Bootstrap, JavaScript, Chart.js
- **Agendamento**: APScheduler

## Requisitos

- Python 3.8+
- Credenciais da API OpenAI
- Credenciais da API Twilio
- Dependências listadas em `requirements.txt`

## Configuração do Ambiente

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/nutriai.git
cd nutriai
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente
```bash
# Crie um arquivo .env na raiz do projeto
OPENAI_API_KEY=sua_chave_openai
TWILIO_ACCOUNT_SID=seu_sid_twilio
TWILIO_AUTH_TOKEN=seu_token_twilio
TWILIO_PHONE_NUMBER=seu_numero_twilio
```

4. Inicialize o banco de dados
```bash
flask db upgrade
```

5. Execute o servidor
```bash
flask run
```

## Integração com WhatsApp

Para usar a integração com WhatsApp:

1. Acesse `/instrucoes-whatsapp` para ver as instruções completas
2. Adicione o número do WhatsApp da Sandbox Twilio aos seus contatos
3. Envie a mensagem de opt-in `join solution-plenty` para iniciar a conversa
4. Após a confirmação, você pode interagir com a IA

## Estrutura do Projeto

```
├── app.py                 # Configuração do app Flask e banco de dados
├── main.py                # Ponto de entrada da aplicação
├── models.py              # Modelos de dados (SQLAlchemy)
├── ai_agent.py            # Lógica do agente de IA
├── notification.py        # Sistema de notificações (SMS/WhatsApp)
├── scheduler.py           # Agendador de tarefas
├── routes.py              # Rotas da aplicação web
├── whatsapp_routes.py     # Rotas específicas do WhatsApp
├── whatsapp_integration.py# Integração com WhatsApp
├── static/                # Arquivos estáticos (CSS, JS)
└── templates/             # Templates HTML
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.