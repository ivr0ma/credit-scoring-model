from pathlib import Path
from typing import Optional

import mlflow.sklearn
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class PatientFeatures(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


class PredictionResponse(BaseModel):
    predict: float


app = FastAPI(
    title="Diabets regression service",
    version="1.0.0",
)

_model: Optional[object] = None


def _get_model_path() -> Path:
    return Path(__file__).resolve().parent / "model"


@app.on_event("startup")
def load_model() -> None:
    """
    Load model saved with mlflow.sklearn.save_model into mlapp/model directory.
    Falls back to dummy predictions if model is not available yet.
    """
    global _model
    model_path = _get_model_path()
    if model_path.exists():
        try:
            _model = mlflow.sklearn.load_model(str(model_path))
        except Exception as exc:  # pragma: no cover - defensive
            # If anything goes wrong, keep the service alive with dummy predictions.
            _model = None
            print(f"Failed to load model from {model_path}: {exc}")
    else:
        _model = None


@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(features: PatientFeatures) -> PredictionResponse:
    """
    Make prediction for a single patient.

    If the trained model is not available yet, returns a deterministic
    pseudo-random value based on input features so that the endpoint
    still works for the first step of the homework.
    """
    vector = np.array(
        [
            [
                features.age,
                features.sex,
                features.bmi,
                features.bp,
                features.s1,
                features.s2,
                features.s3,
                features.s4,
                features.s5,
                features.s6,
            ]
        ],
        dtype=float,
    )

    if _model is None:
        # Deterministic "random-like" fallback so you can test the
        # endpoint before you've trained and exported the model.
        fallback_value = float(vector.sum() * 10.0)
        return PredictionResponse(predict=fallback_value)

    try:
        prediction = _model.predict(vector)[0]
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {exc}")

    return PredictionResponse(predict=float(prediction))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": _model is not None}

