from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from model_wrapper import RFWithThreshold

app = FastAPI(title="API Détection de Fraude Bancaire")

# Charge le modèle entraîné
model = joblib.load("rf_fraude_final_with_threshold.pkl")

class Transaction(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(transaction: Transaction):
    X = np.array([transaction.features])
    result = model.predict(X)
    return {
        "prediction": int(result["predictions"][0]),
        "probability": float(result["probabilities"][0]),
        "alert_human_intervention": bool(result["alerts"][0])
    }
