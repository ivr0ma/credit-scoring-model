FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    jupyterhub==4.1.6 \
    jupyterlab==4.2.5 \
    notebook==7.2.2 \
    configurable-http-proxy \
    oauthenticator \
    pandas numpy scikit-learn matplotlib seaborn mlflow

RUN useradd -m -s /bin/bash admin && \
    echo "admin:admin" | chpasswd

WORKDIR /srv/jupyterhub

COPY jupyterhub_config.py .

EXPOSE 8000

CMD ["jupyterhub", "--config", "/srv/jupyterhub/jupyterhub_config.py"]
