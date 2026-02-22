# app/model.py
import random
from pydantic import BaseModel


# Pydantic модель для валидации входных данных
class ClientFeatures(BaseModel):
    age: int
    income: float
    months_on_book: int
    credit_limit: float


def load_model():
    """Симуляция загрузки модели для табличных данных."""
    print("Загрузка скоринговой модели...")
    return {"version": "1.0-tabular"}


def predict(model: dict, features: ClientFeatures) -> dict:
    """Симуляция предсказания на основе данных клиента."""
    # Ваша логика могла бы быть сложнее, но для ДЗ этого достаточно
    if features.income > 50000 and features.credit_limit > 10000:
        score = random.uniform(0.7, 0.99)
        prediction = "low_risk"
    else:
        score = random.uniform(0.3, 0.69)
        prediction = "high_risk"
    return {"prediction": prediction, "score": round(score, 4)}
