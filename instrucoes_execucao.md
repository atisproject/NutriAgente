# Instruções para Executar o Projeto NutriAI

## Requisitos de Sistema

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)
- Acesso à internet para instalar dependências
- Conta no Twilio com créditos para SMS e WhatsApp
- Conta na OpenAI com API key

## Passos para Executar o Projeto

### 1. Clone o Repositório

```bash
git clone https://github.com/atisproject/nutriagent.git
cd nutriagent
```

### 2. Crie um Ambiente Virtual (recomendado)

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```
Se o arquivo requirements.txt não existir, você pode instalar as dependências manualmente:

```bash
pip install flask flask-sqlalchemy flask-login flask-bootstrap flask-wtf gunicorn openai twilio apscheduler email-validator psycopg2-binary python-dotenv werkzeug
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
OPENAI_API_KEY=sua_chave_openai
TWILIO_ACCOUNT_SID=seu_sid_twilio
TWILIO_AUTH_TOKEN=seu_token_twilio
TWILIO_PHONE_NUMBER=seu_numero_twilio
```

Ou configure as variáveis de ambiente de acordo com seu sistema operacional.

### 5. Inicialize o Banco de Dados

O banco de dados SQLite será criado automaticamente na primeira execução, mas você pode inicializá-lo explicitamente:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6. Execute o Servidor de Desenvolvimento

```bash
python main.py
```

O servidor será iniciado e estará disponível em http://localhost:5000

### 7. Para Ambiente de Produção

Para um ambiente de produção, use Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Configuração do Webhook do Twilio

Para receber mensagens do WhatsApp, você precisa configurar o webhook do Twilio:

1. Acesse o painel do Twilio
2. Vá para Messaging > Try it out > Send a WhatsApp message
3. Configure o Sandbox
4. Configure a URL de Webhook para: `https://seu-dominio.com/whatsapp/webhook`
5. Método: POST

Se estiver testando em ambiente local, use uma ferramenta como ngrok para criar um túnel:

```bash
ngrok http 5000
```

## Acessando a Interface Administrativa

1. Acesse http://localhost:5000 no navegador
2. Faça login com suas credenciais (crie um usuário se necessário)
3. A navegação é feita pelo menu principal

## Solução de Problemas Comuns

### Erro de conexão com API externa

Verifique se as variáveis de ambiente estão configuradas corretamente e se as chaves de API são válidas.

### Erro de banco de dados

Se houver erros relacionados ao banco de dados:
1. Verifique as permissões do diretório onde o banco SQLite está sendo criado
2. Se estiver usando PostgreSQL, verifique a string de conexão

### Erro de dependências

Se houver erros relacionados a dependências ausentes:
1. Verifique se todas as dependências foram instaladas
2. Verifique se as versões das dependências são compatíveis

## Monitoramento e Logs

Para monitorar o sistema em execução, verifique os logs em tempo real:

```bash
# Usando o Linux/macOS
tail -f app.log

# No Windows
Get-Content -Path app.log -Wait
```

## Backup do Banco de Dados

É recomendável fazer backup regular do banco de dados:

```bash
# Para SQLite
cp instance/nutriai.db instance/nutriai.db.backup

# Para PostgreSQL
pg_dump -U username -d nutriai > nutriai_backup.sql
```

## Atualização do Sistema

Para atualizar o sistema a partir do repositório:

```bash
git pull origin main
pip install -r requirements.txt  # Se houver novas dependências
```