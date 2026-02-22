# JupyterHub server + configurable-http-proxy на базе python:3.14-slim
FROM python:3.14-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Системные зависимости: Node.js и npm для configurable-http-proxy
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
        npm \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# JupyterHub и JupyterLab (сервер для пользователей)
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterlab

# configurable-http-proxy — прокси по умолчанию для JupyterHub
RUN npm install -g configurable-http-proxy@^4.2.0 \
    && rm -rf /root/.npm

# Каталог для данных JupyterHub (SQLite, cookie-секреты и т.д.)
RUN mkdir -p /srv/jupyterhub /etc/jupyterhub

WORKDIR /srv/jupyterhub

# Порт прокси (внешний) и порт hub
EXPOSE 8000

# Запуск JupyterHub (прокси поднимается автоматически тем же процессом)
CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
