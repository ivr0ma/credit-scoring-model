FROM python:3.11-slim

RUN pip install --no-cache-dir mlflow==2.19.0 psycopg2-binary boto3

EXPOSE 5000

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri "postgresql://${MLFLOW_DB_USER}:${MLFLOW_DB_PASSWORD}@${MLFLOW_DB_HOST}:${MLFLOW_DB_PORT}/${MLFLOW_DB_NAME}" \
    --default-artifact-root "${MLFLOW_ARTIFACT_ROOT}"
