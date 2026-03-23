from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import numpy as np

from model import AirlinePassengerForecaster

app = FastAPI(
    title="Airline Passengers Forecast API",
    description="Predicts the next month's passenger count from the previous 12 months.",
    version="1.0.0",
)

model = AirlinePassengerForecaster()


class PredictRequest(BaseModel):
    history: List[float] = Field(
        ...,
        min_length=12,
        max_length=12,
        description="Exactly 12 monthly passenger counts in chronological order."
    )


class PredictResponse(BaseModel):
    input_window: List[float]
    predicted_next_month: float
    model_name: str
    units: str = "monthly passengers"


@app.get("/")
def root():
    return {
        "message": "Airline Passengers Forecast API",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": model.model_name}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    try:
        pred = model.predict_next(payload.history)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PredictResponse(
        input_window=payload.history,
        predicted_next_month=round(float(pred), 2),
        model_name=model.model_name,
    )
