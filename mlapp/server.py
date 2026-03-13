from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics


app = FastAPI(title="ML Service with Monitoring")

# Подключаем Prometheus middleware и эндпоинт /metrics
app.add_middleware(
    PrometheusMiddleware,
    app_name="ml_service",
    prefix="ml_service",
    group_paths=True,
)
app.add_route("/metrics", handle_metrics)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/predict")
async def predict():
    # Заглушка для примера; здесь должен быть вызов ML модели
    return {"prediction": 0}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

