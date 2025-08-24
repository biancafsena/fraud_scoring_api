from pydantic import BaseModel, Field
from typing import Literal

class Transaction(BaseModel):
    amount: float = Field(..., ge=0)
    merchant_risk_score: float = Field(..., ge=0, le=1)
    device_trust_score: float = Field(..., ge=0, le=1)
    channel: Literal["CARD", "PIX", "WEB", "APP"]
    hour: int = Field(..., ge=0, le=23)
    country: Literal["BR", "CL", "MX", "AR"]
    user_txn_24h: int = Field(..., ge=0)

class PredictionResponse(BaseModel):
    fraud_probability: float
    is_fraud: bool
