# Documentação do Projeto NutriAI

## Sumário

1. [Introdução](#1-introdução)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Funcionalidades Principais](#3-funcionalidades-principais)
4. [Modelo de Dados](#4-modelo-de-dados)
5. [Integração com IA](#5-integração-com-ia)
6. [Sistema de Notificações](#6-sistema-de-notificações)
7. [Integração com WhatsApp](#7-integração-com-whatsapp)
8. [Interface Administrativa](#8-interface-administrativa)
9. [Agendador de Tarefas](#9-agendador-de-tarefas)
10. [Configuração do Ambiente](#10-configuração-do-ambiente)
11. [Guia de Manutenção](#11-guia-de-manutenção)

## 1. Introdução

O NutriAI é um sistema automatizado de conversão de leads para empresas de nutrição. Utiliza inteligência artificial para personalizar conversas, esclarecer dúvidas e vender produtos automaticamente. O sistema funciona 24 horas por dia, 7 dias por semana, oferecendo atendimento contínuo aos clientes.

### 1.1 Objetivos do Projeto

- Automatizar o atendimento inicial de clientes potenciais
- Qualificar leads através de conversas personalizadas
- Coletar informações importantes sobre os clientes
- Aumentar a taxa de conversão de leads em clientes
- Reduzir o trabalho manual de acompanhamento de leads
- Fornecer uma interface amigável para gerenciamento de leads

### 1.2 Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Banco de Dados**: SQLAlchemy com SQLite/PostgreSQL
- **Inteligência Artificial**: OpenAI API (GPT-4)
- **Mensagens**: Twilio API para SMS e WhatsApp
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Agendamento**: APScheduler

## 2. Arquitetura do Sistema

O sistema foi desenvolvido seguindo uma arquitetura MVC (Model-View-Controller) usando o framework Flask. A aplicação é composta por diversos módulos e componentes que trabalham em conjunto.

### 2.1 Estrutura de Diretórios

```
├── instance/              # Banco de dados SQLite
├── static/                # Arquivos estáticos (CSS, JS)
│   ├── css/
│   │   └── custom.css
│   └── js/
│       ├── chat.js
│       └── dashboard.js
├── templates/             # Templates HTML
│   ├── layout.html        # Template base
│   ├── index.html         # Página inicial
│   ├── dashboard.html     # Dashboard administrativo
│   ├── leads.html         # Lista de leads
│   ├── detalhe_lead.html  # Detalhes de um lead
│   ├── configuracoes.html # Configurações do sistema
│   └── ...
├── app.py                 # Configuração do Flask e DB
├── main.py                # Ponto de entrada da aplicação
├── models.py              # Modelos de dados
├── routes.py              # Rotas principais da aplicação
├── ai_agent.py            # Lógica do agente de IA
├── notification.py        # Sistema de notificações
├── scheduler.py           # Agendador de tarefas
├── whatsapp_integration.py# Integração com WhatsApp
└── whatsapp_routes.py     # Rotas para webhook do WhatsApp
```

### 2.2 Fluxo de Dados

1. **Captura de Leads**: Através de formulários web ou mensagens via WhatsApp
2. **Processamento de Mensagens**: O sistema processa as mensagens usando IA
3. **Armazenamento**: As informações são armazenadas no banco de dados
4. **Notificações**: Envio de SMS ou mensagens WhatsApp aos clientes
5. **Agendamento**: Tarefas automáticas para acompanhamento de leads
6. **Interface Administrativa**: Visualização e gerenciamento dos dados

## 3. Funcionalidades Principais

### 3.1 Agente de IA

- Processa mensagens dos clientes usando o modelo GPT-4 da OpenAI
- Personaliza respostas com base no histórico de interações
- Extrai informações relevantes das mensagens
- Analisa sentimento e interesse do cliente
- Esclarece dúvidas sobre produtos e serviços
- Sugere produtos adequados ao perfil do cliente

### 3.2 Gestão de Leads

- Cadastro automático de novos leads
- Categorização por status (novo, em contato, convertido, perdido)
- Histórico completo de interações
- Visualização de dados de formulários respondidos
- Atribuição de leads a atendentes humanos
- Estatísticas de conversão

### 3.3 Sistema de Formulários

- Envio automático de formulários (anamnese, avaliação física)
- Lembretes para formulários pendentes
- Processamento de respostas
- Análise dos dados coletados

### 3.4 Base de Conhecimento

- Cadastro de informações sobre produtos e serviços
- Perguntas frequentes e suas respostas
- Informações nutricionais de referência
- Utilizada pelo agente de IA para responder perguntas

### 3.5 Dashboard Administrativo

- Visão geral de métricas e indicadores
- Gráficos de desempenho
- Lista de leads recentes
- Alertas sobre leads com alta chance de conversão

## 4. Modelo de Dados

### 4.1 Principais Entidades

#### 4.1.1 User (Usuário)
- Administradores e atendentes do sistema
- Atributos: id, username, email, password_hash, role, created_at
- Relacionamentos: leads (one-to-many)

#### 4.1.2 Lead
- Potenciais clientes capturados pelo sistema
- Atributos: id, nome, email, telefone, status, fonte, user_id, criado_em, atualizado_em
- Relacionamentos: interacoes (one-to-many), formularios (one-to-many), user (many-to-one)

#### 4.1.3 Interacao
- Registro de mensagens trocadas com o lead
- Atributos: id, lead_id, mensagem, origem (ia, usuario, sistema), data_hora
- Relacionamentos: lead (many-to-one)

#### 4.1.4 Formulario
- Formulários enviados aos leads
- Atributos: id, lead_id, tipo, status, data_envio, data_resposta, lembrete_enviado
- Relacionamentos: lead (many-to-one)

#### 4.1.5 ProdutoNutricao
- Produtos e serviços oferecidos
- Atributos: id, nome, descricao, preco, categoria, ativo
- Sem relacionamentos diretos

#### 4.1.6 BaseConhecimento
- Conhecimento utilizado pelo agente de IA
- Atributos: id, tema, conteudo, tipo, criado_em, atualizado_em
- Sem relacionamentos diretos

#### 4.1.7 Configuracao
- Configurações gerais do sistema
- Atributos: id, chave, valor, descricao
- Sem relacionamentos diretos

### 4.2 Diagrama de Relacionamentos

```
User (1) ----< Lead (n)
Lead (1) ----< Interacao (n)
Lead (1) ----< Formulario (n)
```

## 5. Integração com IA

A integração com IA é um componente central do sistema, implementada no módulo `ai_agent.py`.

### 5.1 Funcionamento do Agente

1. **Carregamento da Base de Conhecimento**: O sistema carrega todas as informações relevantes da base de conhecimento
2. **Geração de Contexto**: Criação de um contexto personalizado para o modelo de IA
3. **Processamento de Mensagens**: As mensagens são enviadas para a API OpenAI com o contexto adequado
4. **Tratamento de Respostas**: As respostas são processadas e enviadas ao cliente

### 5.2 Funções Principais

- `carregar_base_conhecimento()`: Carrega toda a base de conhecimento para o contexto do agente
- `gerar_contexto_sistema()`: Gera o contexto do sistema para o agente de IA
- `agente_boas_vindas(nome)`: Agente de boas-vindas para primeiro contato com o lead
- `processar_mensagem(lead_id, mensagem_cliente)`: Processa a mensagem do cliente e gera uma resposta adequada
- `gerar_lembrete_formulario(lead_id, formulario_tipo)`: Gera um lembrete personalizado para formulários não respondidos
- `analisar_sentimento_cliente(mensagem)`: Analisa o sentimento do cliente na mensagem

## 6. Sistema de Notificações

O sistema de notificações é implementado no módulo `notification.py` e utiliza a API do Twilio para enviar mensagens SMS e WhatsApp.

### 6.1 Principais Funções

- `formatar_numero_internacional(numero)`: Formata um número para o padrão internacional (+55)
- `enviar_sms(numero_destino, mensagem)`: Envia uma mensagem SMS
- `enviar_whatsapp(numero_destino, mensagem)`: Envia uma mensagem WhatsApp
- `notificar_administrador(assunto, conteudo, via_whatsapp)`: Envia uma notificação para o administrador
- `notificar_novo_lead(nome, telefone)`: Notifica sobre um novo lead
- `notificar_formulario_pendente(nome, telefone, tipo_formulario, dias_pendente)`: Notifica sobre formulários pendentes
- `notificar_potencial_conversao(nome, telefone, probabilidade)`: Notifica sobre leads com alta probabilidade de conversão

### 6.2 Configuração do Canal de Comunicação

O sistema permite escolher entre SMS e WhatsApp como canal padrão de comunicação, podendo ser configurado na interface administrativa. A escolha pode ser sobrescrita pela origem do lead.

## 7. Integração com WhatsApp

A integração com WhatsApp é implementada nos módulos `whatsapp_integration.py` e `whatsapp_routes.py`.

### 7.1 Sandbox do WhatsApp Business API

O sistema utiliza o ambiente sandbox do WhatsApp Business API através do Twilio. Para isso, foi criada uma página de instruções para que os usuários possam fazer o opt-in e começar a usar o serviço.

### 7.2 Principais Funcionalidades

- Recebimento de mensagens via webhook
- Processamento de mensagens com IA
- Identificação automática de novos leads
- Extração de nomes a partir das mensagens
- Registro de interações no banco de dados
- Análise de sentimento para identificar oportunidades de conversão

### 7.3 Fluxo de Comunicação

1. Cliente envia mensagem para o número do WhatsApp
2. Twilio encaminha a mensagem para o webhook
3. Sistema processa a mensagem e identifica o lead
4. Agente de IA gera uma resposta personalizada
5. Sistema envia a resposta de volta para o cliente
6. Todas as interações são registradas no banco de dados

## 8. Interface Administrativa

A interface administrativa permite gerenciar todos os aspectos do sistema através de uma interface web amigável.

### 8.1 Páginas Principais

- **Dashboard**: Visão geral de métricas e indicadores
- **Leads**: Lista de leads e acesso aos detalhes
- **Detalhe do Lead**: Informações completas e histórico de interações
- **Base de Conhecimento**: Gestão de conteúdos para o agente de IA
- **Configurações**: Configurações gerais do sistema

### 8.2 Configurações Disponíveis

- Informações da empresa (nome, telefone, email)
- Horário de atendimento
- Modelos de mensagens (boas-vindas, lembretes, reativação)
- Configurações de formulários (dias para lembrete, máximo de lembretes)
- Canal de comunicação padrão (SMS ou WhatsApp)
- Telefone para notificações
- Tipos de notificações (novos leads, formulários pendentes, conversões)

## 9. Agendador de Tarefas

O sistema utiliza um agendador de tarefas implementado no módulo `scheduler.py` utilizando a biblioteca APScheduler.

### 9.1 Tarefas Agendadas

- **Verificação de Formulários Pendentes**: Envia lembretes para formulários não respondidos após um determinado período
- **Verificação de Leads Inativos**: Envia mensagens de reativação para leads sem interação recente

### 9.2 Configuração do Agendador

- Armazenamento de jobs no banco de dados (SQLAlchemyJobStore)
- Execução em threads separadas (ThreadPoolExecutor)
- Intervalo de execução configurável
- Inicialização automática com a aplicação

## 10. Configuração do Ambiente

### 10.1 Requisitos

- Python 3.8 ou superior
- Bibliotecas Python (ver requirements.txt)
- Conta na OpenAI com API key
- Conta no Twilio com créditos para SMS e WhatsApp

### 10.2 Variáveis de Ambiente

```
OPENAI_API_KEY=sua_chave_openai
TWILIO_ACCOUNT_SID=seu_sid_twilio
TWILIO_AUTH_TOKEN=seu_token_twilio
TWILIO_PHONE_NUMBER=seu_numero_twilio
```

### 10.3 Inicialização

1. Configure as variáveis de ambiente
2. Execute `python main.py` para iniciar o servidor
3. Acesse http://localhost:5000 no navegador

## 11. Guia de Manutenção

### 11.1 Atualização da Base de Conhecimento

A base de conhecimento deve ser atualizada regularmente para garantir que o agente de IA tenha acesso às informações mais recentes. Isso pode ser feito através da interface administrativa.

### 11.2 Monitoramento de Leads

O sistema registra todas as interações com leads, mas é importante monitorar regularmente o dashboard para identificar leads com alta probabilidade de conversão que possam precisar de atendimento humano.

### 11.3 Verificação de Lembretes

O agendador de tarefas envia lembretes automaticamente, mas é importante verificar se estão funcionando corretamente. O log do sistema registra todas as atividades do agendador.

### 11.4 Backup do Banco de Dados

Recomenda-se fazer backup regular do banco de dados para evitar perda de informações importantes.

### 11.5 Atualização do Modelo de IA

Quando novos modelos de IA estiverem disponíveis, pode ser necessário atualizar o código para utilizá-los, ajustando os parâmetros de acordo com as especificações do novo modelo.