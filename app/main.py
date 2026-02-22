from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from app.model import ClientFeatures, load_model, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загрузка модели при старте приложения."""
    app.state.model = load_model()
    yield
    app.state.model = None


app = FastAPI(
    title="Credit Scoring API",
    description="REST API для оценки кредитного риска заёмщика (заглушка для ДЗ 3)",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    """Эндпоинт проверки работоспособности сервиса."""
    return {"status": "ok"}


@app.post("/predict", response_model=dict)
def predict_risk(request: Request, features: ClientFeatures):
    """
    Предсказание кредитного риска по данным заёмщика.

    - **age**: возраст (целое число)
    - **income**: доход (число с плавающей точкой)
    - **months_on_book**: срок в месяцах как клиент банка
    - **credit_limit**: кредитный лимит

    Возвращает prediction (low_risk / high_risk) и score (0–1).
    """
    model = getattr(request.app.state, "model", None)
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        result = predict(model, features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
