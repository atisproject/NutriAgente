# Guia de Configuração do NutriAI no GitHub Codespaces

Este guia apresenta um passo a passo detalhado para configurar e executar o sistema NutriAI utilizando o GitHub Codespaces.

## 1. Criar um Repositório no GitHub

Primeiro, você precisa ter um repositório no GitHub:

1. Acesse [GitHub](https://github.com) e faça login na sua conta
2. Clique no botão "+" no canto superior direito e selecione "New repository"
3. Preencha:
   - Nome do repositório: `nutriai` (ou outro nome de sua preferência)
   - Descrição: "Sistema de IA para nutrição com atendimento automatizado"
   - Visibilidade: Pública ou Privada (recomendado privado para proteger dados sensíveis)
   - Inicialize com README: Sim
4. Clique em "Create repository"

## 2. Transferir os Arquivos do Projeto para o GitHub

### Opção 1: Diretamente do Replit para o GitHub

1. No Replit, baixe o código como ZIP:
   - Clique nos três pontos (⋯) no canto superior esquerdo
   - Selecione "Download as zip"
   - Salve o arquivo ZIP no seu computador

2. No GitHub, vá para o repositório criado e:
   - Clique no botão "Add file" e selecione "Upload files"
   - Extraia os arquivos do ZIP no seu computador
   - Arraste e solte os arquivos importantes do projeto no GitHub
   - Adicione uma mensagem de commit como "Versão inicial do NutriAI"
   - Clique em "Commit changes"

### Opção 2: Usando Git no seu Computador

1. Clone o repositório vazio para seu computador:
   ```bash
   git clone https://github.com/seu-usuario/nutriai.git
   cd nutriai
   ```

2. Extraia os arquivos do ZIP baixado do Replit e copie-os para a pasta clonada

3. Adicione, commite e faça push dos arquivos:
   ```bash
   git add .
   git commit -m "Versão inicial do NutriAI"
   git push origin main
   ```

## 3. Iniciar um Codespace no Repositório

1. Vá para seu repositório no GitHub
2. Clique no botão "Code" (verde)
3. Na aba "Codespaces", clique em "Create codespace on main"
4. Aguarde enquanto o Codespace é criado e inicializado (isso pode levar alguns minutos)

## 4. Configurar o Ambiente no Codespace

Uma vez que o Codespace esteja aberto:

1. Abra o terminal do Codespace clicando em "Terminal" > "New Terminal" no menu superior

2. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r dependencias.txt
   ```

4. Configure as variáveis de ambiente sensíveis:
   ```bash
   # Crie um arquivo .env para armazenar as variáveis de ambiente
   touch .env
   ```

5. Edite o arquivo .env no editor:
   - Clique no arquivo .env no explorador de arquivos
   - Adicione as seguintes linhas:
   ```
   OPENAI_API_KEY=sua_chave_da_openai
   TWILIO_ACCOUNT_SID=seu_sid_do_twilio
   TWILIO_AUTH_TOKEN=seu_token_do_twilio
   TWILIO_PHONE_NUMBER=seu_numero_do_twilio
   ```
   - Substitua os valores pelas suas credenciais reais

## 5. Configurar Secrets do Codespace (Alternativa mais segura)

Em vez de usar um arquivo .env, você pode configurar secrets no Codespace:

1. No GitHub, vá para seu repositório
2. Clique em "Settings" > "Secrets and variables" > "Codespaces"
3. Clique em "New repository secret"
4. Adicione cada uma das variáveis de ambiente:
   - Nome: `OPENAI_API_KEY`, Valor: sua_chave_da_openai
   - Nome: `TWILIO_ACCOUNT_SID`, Valor: seu_sid_do_twilio
   - Nome: `TWILIO_AUTH_TOKEN`, Valor: seu_token_do_twilio
   - Nome: `TWILIO_PHONE_NUMBER`, Valor: seu_numero_do_twilio
5. Clique em "Add secret" para cada um

Esses secrets estarão disponíveis como variáveis de ambiente no seu Codespace.

## 6. Inicializar o Banco de Dados

No terminal do Codespace, execute:

```bash
# Ative o ambiente virtual se ainda não estiver ativado
source venv/bin/activate

# Inicialize o banco de dados
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 7. Executar o Servidor de Desenvolvimento

```bash
python main.py
```

## 8. Acessar a Aplicação

1. O Codespace exibirá uma notificação de que um serviço está em execução na porta 5000
2. Clique em "Open in Browser" para abrir a aplicação no navegador
3. Você também pode clicar em "Ports" na parte inferior do VS Code, localizar a porta 5000 e clicar no ícone do globo para abrir no navegador

## 9. Configurar Webhook do Twilio para o Codespace

Para receber mensagens do WhatsApp, você precisa configurar o webhook do Twilio:

1. No Codespace, a aplicação estará acessível através de uma URL pública temporária, algo como:
   `https://seu-codespace-nome-xxxx-5000.preview.app.github.dev/`

2. Copie esta URL e adicione o caminho do webhook: 
   `https://seu-codespace-nome-xxxx-5000.preview.app.github.dev/whatsapp/webhook`

3. No painel do Twilio:
   - Vá para Messaging > Try it out > Send a WhatsApp message
   - Configure o Sandbox
   - Configure a URL de Webhook para a URL completa copiada
   - Método: POST

## 10. Dicas para Trabalhar com Codespaces

### Persistência de Dados

- O banco de dados SQLite será armazenado dentro do Codespace
- Se quiser preservar os dados, faça backup regularmente:
  ```bash
  cp instance/nutriai.db /workspaces/nutriai/backups/nutriai_backup_$(date +%Y%m%d).db
  ```

### Fazer Commit das Alterações

Para salvar alterações no seu repositório:

```bash
git add .
git commit -m "Descrição das alterações"
git push origin main
```

### Reabrindo o Codespace

Se fechar o Codespace, você pode reabri-lo mais tarde:

1. Vá para [github.com/codespaces](https://github.com/codespaces)
2. Encontre seu Codespace na lista e clique nele
3. Após reabrir, você precisará reativar o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```
4. E iniciar o servidor novamente:
   ```bash
   python main.py
   ```

## 11. Solução de Problemas Comuns

### Erro de Porta em Uso

Se receber um erro de que a porta 5000 já está em uso:

```bash
lsof -i :5000  # Verificar qual processo está usando a porta
kill -9 [PID]  # Substitua [PID] pelo número do processo
```

### Erro de Permissão no Banco de Dados

Se encontrar erros de permissão no banco de dados:

```bash
chmod 666 instance/nutriai.db
```

### Erros de Variáveis de Ambiente

Se a aplicação não conseguir acessar as variáveis de ambiente:

1. Verifique se o arquivo .env está presente e tem as variáveis corretas
2. Ou verifique se os secrets do Codespace estão configurados corretamente
3. Tente carregar manualmente as variáveis no terminal:
   ```bash
   export OPENAI_API_KEY=sua_chave_da_openai
   export TWILIO_ACCOUNT_SID=seu_sid_do_twilio
   export TWILIO_AUTH_TOKEN=seu_token_do_twilio
   export TWILIO_PHONE_NUMBER=seu_numero_do_twilio
   ```

### Erro de Módulo Não Encontrado

Se encontrar erros de "module not found":

```bash
pip install -r dependencias.txt  # Reinstale as dependências
```