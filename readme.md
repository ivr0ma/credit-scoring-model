# Credit Scoring Model — DataOps

ML-сервис кредитного скоринга с полным циклом MLOps: от трекинга экспериментов до деплоя в Kubernetes.

## Структура проекта

```
.
├── mlflow/              # Этап 1: MLflow tracking server
├── airflow/             # Этап 2: Airflow оркестрация пайплайнов
├── lakefs/              # Этап 3: LakeFS версионирование данных
├── jupyterhub/          # Этап 4: JupyterHub среда разработки
├── ml-service/          # Этап 5–6: ML-сервис + мониторинг
│   ├── app/             # FastAPI приложение
│   ├── grafana/         # Grafana provisioning
│   ├── prometheus.yml   # Конфигурация Prometheus
│   └── docker-compose.yaml
├── k8s/                 # Этап 7: Kubernetes манифесты
├── helm/                # Этап 8: Helm chart
└── mlflow-prompts/      # Этап 9: MLflow Prompt Storage
```

## Компоненты

### 1. MLflow

Трекинг-сервер для логирования экспериментов и артефактов. Backend — PostgreSQL.

```bash
cd mlflow
docker compose up -d
```

Веб-интерфейс: http://localhost:5000

---

### 2. Airflow

Оркестратор ML-пайплайнов. Включает DAG `credit_scoring_pipeline` с шагами: загрузка данных → предобработка → обучение → оценка.

```bash
cd airflow
docker compose up -d
```

Веб-интерфейс: http://localhost:8080 (admin / admin)

---

### 3. LakeFS

Версионирование данных на базе MinIO (S3-совместимое хранилище) и PostgreSQL.

```bash
cd lakefs
docker compose up -d
```

| Сервис | URL | Логин |
|--------|-----|-------|
| LakeFS | http://localhost:8001 | AKIAIOSFODNN7EXAMPLE |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin_secret |

---

### 4. JupyterHub

Многопользовательская среда для разработки и исследований.

```bash
cd jupyterhub
docker compose up -d
```

Веб-интерфейс: http://localhost:8888 (admin / admin)

---

### 5 & 6. ML-сервис + Мониторинг

FastAPI сервис кредитного скоринга на базе `GradientBoostingClassifier`. Включает Prometheus и Grafana.

```bash
cd ml-service
docker compose up -d
```

| Сервис | URL |
|--------|-----|
| ML-сервис API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin / admin) |

**Пример запроса:**

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 80000,
    "loan_amount": 20000,
    "loan_term": 60,
    "credit_history_length": 120,
    "num_credit_lines": 3,
    "employment_years": 8,
    "debt_to_income": 0.3
  }'
```

**Ответ:**

```json
{
  "score": 0.7842,
  "decision": "approved",
  "model_version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Доступные эндпоинты:**

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/predict` | Предсказание кредитного скоринга |
| GET | `/metrics` | Метрики Prometheus |
| GET | `/health` | Healthcheck |

---

### 7. Kubernetes манифесты

```
k8s/
├── deployment.yaml   # 2 реплики, startup/readiness/liveness probes
├── service.yaml      # ClusterIP сервис
├── ingress.yaml      # Nginx ingress (credit-scoring.example.com)
└── secret.yaml       # Database URL
```

```bash
kubectl apply -f k8s/
```

---

### 8. Helm Chart

```bash
helm install credit-scoring ./helm/credit-scoring

# Изменить версию образа:
helm upgrade credit-scoring ./helm/credit-scoring --set image.tag=2.0.0

# Изменить ресурсы:
helm upgrade credit-scoring ./helm/credit-scoring \
  --set resources.limits.cpu=1000m \
  --set resources.limits.memory=1Gi
```

---

### 9. MLflow Prompt Storage

Создание 5 версий промптов (кредитный скоринг v1/v2, русская версия, объяснение решения, детектирование мошенничества):

```bash
cd mlflow-prompts
MLFLOW_TRACKING_URI=http://localhost:5000 python create_prompts.py
```

## Переменные окружения

Каждый компонент имеет свой `.env` файл. Перед запуском в продакшене замените секреты на надёжные значения.

| Компонент | Файл |
|-----------|------|
| MLflow | `mlflow/.env` |
| Airflow | `airflow/.env` |
| LakeFS | `lakefs/.env` |
| JupyterHub | `jupyterhub/.env` |
| ML-сервис | `ml-service/.env` |
