from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    input_data = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    decision = Column(String(20), nullable=False)
    model_version = Column(String(50), nullable=False)
    latency_ms = Column(Float, nullable=False)
