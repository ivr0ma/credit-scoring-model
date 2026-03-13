DataOps – HW24: Полноценный ML-сервис (диабет)

### Структура проекта

- `research/train.ipynb` – ноутбук с обучением `RandomForestRegressor` на датасете диабета, логированием в MLflow, регистрацией модели под именем `diabets` и экспортом в `mlapp/model` для сервиса.
- `mlapp/server.py`, `mlapp/__main__.py` – исходники FastAPI ML-сервиса.
- `requirements.txt` – зависимости проекта.
- `Dockerfile` – Docker-образ сервиса.
- `docker-compose.yaml` – docker-compose для запуска ML-сервиса.
- `curl_examples.txt` – примеры вызовов REST ручки `predict`.

### Шаги для воспроизведения

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Запустить MLflow Tracking Server (пример):

```bash
mlflow ui --backend-store-uri sqlite:///mlruns.db --default-artifact-root ./mlruns
```

3. Запустить Jupyter Lab и выполнить ноутбук `research/train.ipynb` по шагам, чтобы:
- обучить модель,
- залогировать и зарегистрировать её в MLflow под именем `diabets`,
- загрузить нужную версию через `mlflow.sklearn.load_model`,
- сохранить модель в `mlapp/model`.

4. Запустить FastAPI сервис локально:

```bash
python -m mlapp
```

или через Docker Compose:

```bash
docker compose up --build
```

5. Воспользоваться примерами из `curl_examples.txt` (или любым REST-клиентом, например Bruno) для вызова:
- `GET /health`
- `POST /api/v1/predict`
