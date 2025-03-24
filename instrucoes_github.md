# Instruções para transferir o código para o GitHub

## Opção 1: Clonando o repositório e copiando os arquivos

1. Clone o repositório vazio no seu computador:
   ```bash
   git clone https://github.com/atisproject/nutriagent.git
   cd nutriagent
   ```

2. Baixe os arquivos do projeto do Replit:
   - No Replit, clique no menu de três pontos (⋯) no canto superior esquerdo
   - Selecione "Download as zip"
   - Extraia o arquivo ZIP no seu computador

3. Copie todos os arquivos importantes do projeto para a pasta do repositório clonado:
   - ai_agent.py
   - app.py
   - documentacao.md
   - main.py
   - models.py
   - notification.py
   - pyproject.toml
   - README.md
   - routes.py
   - scheduler.py
   - static/ (pasta)
   - templates/ (pasta)
   - whatsapp_integration.py
   - whatsapp_routes.py
   - .gitignore

4. Adicione, commite e faça push dos arquivos para o GitHub:
   ```bash
   git add .
   git commit -m "Versão inicial do NutriAI - Sistema Inteligente de Nutrição"
   git push origin main
   ```

## Opção 2: Usando o GitHub CLI

Se você tem o GitHub CLI instalado:

1. Clone o repositório:
   ```bash
   git clone https://github.com/atisproject/nutriagent.git
   cd nutriagent
   ```

2. Baixe os arquivos do Replit conforme a Opção 1, passo 2.

3. Copie os arquivos conforme a Opção 1, passo 3.

4. Adicione, commite e faça push como na Opção 1, passo 4.

## Opção 3: Upload direto pelo GitHub

1. Acesse https://github.com/atisproject/nutriagent no seu navegador

2. Se o repositório estiver vazio, você verá uma opção para fazer upload de arquivos

3. Baixe os arquivos do Replit conforme a Opção 1, passo 2

4. No GitHub, arraste e solte os arquivos ou use o botão "upload files" para cada um dos arquivos principais listados na Opção 1, passo 3

5. Adicione uma mensagem de commit e faça o commit diretamente para a branch main

## Arquivos importantes para transferir

Certifique-se de transferir todos estes arquivos:

- **Arquivos Python**:
  - ai_agent.py
  - app.py
  - main.py
  - models.py 
  - notification.py
  - routes.py
  - scheduler.py
  - whatsapp_integration.py
  - whatsapp_routes.py

- **Documentação**:
  - README.md
  - documentacao.md

- **Configuração**:
  - pyproject.toml
  - .gitignore

- **Pastas**:
  - static/ (CSS, JS)
  - templates/ (HTML)

Observação: Não transfira arquivos sensíveis como variáveis de ambiente (.env) ou outros arquivos que contenham senhas ou chaves de API.

## Depois da transferência

Depois de transferir os arquivos para o GitHub, você precisará configurar as variáveis de ambiente no ambiente onde for executar o sistema:

- OPENAI_API_KEY
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER

Esses valores não devem ser commitados no repositório por questões de segurança.