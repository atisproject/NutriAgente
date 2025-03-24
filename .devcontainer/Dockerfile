FROM python:3.11-slim

# Evita que Python crie arquivos .pyc no container
ENV PYTHONDONTWRITEBYTECODE=1
# Evita buffer de saída para logs
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala ferramentas de desenvolvimento Python
RUN pip install --upgrade pip \
    && pip install black flake8 pytest

# Copia arquivos de requisitos
COPY dependencias.txt .

# Instala dependências do projeto
RUN pip install -r dependencias.txt

# Define o comando padrão
CMD ["bash"]