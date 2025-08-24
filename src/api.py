from fastapi import FastAPI
from .schema import Transaction, PredictionResponse
from .utils import load_model_and_features, to_model_df, predict_proba

app = FastAPI(title="Fraud Scoring API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict(txn: Transaction):
    model, feature_names = load_model_and_features()
    X = to_model_df(txn, feature_names)
    p = float(predict_proba(model, X))
    return {"fraud_probability": p, "is_fraud": p >= 0.5}
