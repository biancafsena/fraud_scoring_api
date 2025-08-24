import json, os
from pathlib import Path
import pandas as pd
import joblib
from typing import Tuple, List
from pydantic import BaseModel

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"
FEATS_PATH = MODEL_DIR / "feature_names.json"

def ensure_paths():
    MODEL_DIR.mkdir(exist_ok=True, parents=True)

def save_model(model, feature_names: list):
    ensure_paths()
    joblib.dump(model, MODEL_PATH)
    with open(FEATS_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, ensure_ascii=False, indent=2)

def load_model_and_features():
    if not MODEL_PATH.exists() or not FEATS_PATH.exists():
        raise RuntimeError("Modelo não encontrado. Rode: python -m src.train")
    model = joblib.load(MODEL_PATH)
    with open(FEATS_PATH, "r", encoding="utf-8") as f:
        feats = json.load(f)
    return model, feats

def to_model_df(txn: BaseModel, feature_names: list) -> pd.DataFrame:
    df = pd.DataFrame([txn.model_dump()])

    # one-hot encoders (manuais para manter simples e estável)
    df = pd.get_dummies(df, columns=["channel","country"], drop_first=False)

    # garantir colunas na ordem do treino
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_names]
    return df

def predict_proba(model, X: pd.DataFrame) -> float:
    proba = model.predict_proba(X)[0,1]
    return proba
