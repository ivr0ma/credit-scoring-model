import time
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import joblib
import os

from .database import engine, Base, SessionLocal
from .models import PredictionLog
from .ml_model import CreditScoringModel

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'credit_scoring_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'credit_scoring_request_duration_seconds',
    'Request latency in seconds',
    ['endpoint']
)
PREDICTION_SCORE = Histogram(
    'credit_scoring_prediction_score',
    'Distribution of credit scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)
MODEL_VERSION_GAUGE = Gauge(
    'credit_scoring_model_version',
    'Current model version',
    ['version']
)

MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
model = CreditScoringModel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    MODEL_VERSION_GAUGE.labels(version=MODEL_VERSION).set(1)
    logger.info(json.dumps({"event": "startup", "model_version": MODEL_VERSION}))
    yield
    logger.info(json.dumps({"event": "shutdown"}))


app = FastAPI(
    title="Credit Scoring Service",
    version=MODEL_VERSION,
    lifespan=lifespan
)


class CreditFeatures(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    income: float = Field(..., gt=0, description="Annual income")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_term: int = Field(..., ge=1, le=360, description="Loan term in months")
    credit_history_length: int = Field(..., ge=0, description="Credit history in months")
    num_credit_lines: int = Field(..., ge=0, description="Number of existing credit lines")
    employment_years: float = Field(..., ge=0, description="Years of employment")
    debt_to_income: float = Field(..., ge=0, le=1, description="Debt to income ratio")


class PredictionResponse(BaseModel):
    score: float
    decision: str
    model_version: str
    timestamp: str


@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": MODEL_VERSION}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(features: CreditFeatures):
    start_time = time.time()
    timestamp = datetime.utcnow().isoformat()

    try:
        input_data = np.array([[
            features.age,
            features.income,
            features.loan_amount,
            features.loan_term,
            features.credit_history_length,
            features.num_credit_lines,
            features.employment_years,
            features.debt_to_income,
        ]])

        score = model.predict(input_data)[0]
        decision = "approved" if score >= 0.5 else "rejected"

        PREDICTION_SCORE.observe(score)
        REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/predict", status="200").inc()

        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint="/api/v1/predict").observe(latency)

        logger.info(json.dumps({
            "event": "prediction",
            "input": features.model_dump(),
            "score": score,
            "decision": decision,
            "latency_ms": round(latency * 1000, 2),
            "model_version": MODEL_VERSION,
            "timestamp": timestamp,
        }))

        # Log to DB
        db = SessionLocal()
        try:
            log_entry = PredictionLog(
                timestamp=datetime.utcnow(),
                input_data=json.dumps(features.model_dump()),
                score=score,
                decision=decision,
                model_version=MODEL_VERSION,
                latency_ms=round(latency * 1000, 2),
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_err:
            logger.warning(json.dumps({"event": "db_log_failed", "error": str(db_err)}))
        finally:
            db.close()

        return PredictionResponse(
            score=round(score, 4),
            decision=decision,
            model_version=MODEL_VERSION,
            timestamp=timestamp,
        )

    except Exception as e:
        REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/predict", status="500").inc()
        logger.error(json.dumps({"event": "prediction_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail=str(e))
