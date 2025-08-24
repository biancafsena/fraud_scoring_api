import argparse, numpy as np, pandas as pd, random
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.ensemble import GradientBoostingClassifier
from .utils import save_model

def make_synth(n_samples: int = 50000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    channels = np.array(["CARD","PIX","WEB","APP"])
    countries = np.array(["BR","CL","MX","AR"])

    amount = rng.gamma(shape=2.0, scale=150.0, size=n_samples)  # valores positivos assimétricos
    merchant_risk = rng.uniform(0, 1, size=n_samples)
    device_trust = rng.uniform(0, 1, size=n_samples)
    hour = rng.integers(0, 24, size=n_samples)
    user_txn_24h = rng.poisson(lam=3.5, size=n_samples)

    channel = rng.choice(channels, size=n_samples, p=[0.5, 0.2, 0.2, 0.1])
    country = rng.choice(countries, size=n_samples, p=[0.7, 0.1, 0.1, 0.1])

    # regra de fraude: valores altos, madrugada (0–4), baixo device_trust, alto merchant_risk, canal PIX/web
    base_logit = (
        0.002*(amount - 300) +
        2.0*(merchant_risk - 0.6) +
        -2.5*(device_trust - 0.4) +
        0.25*((hour >= 0) & (hour <= 4)).astype(float) +
        0.15*(user_txn_24h - 3) +
        0.5*(channel == "PIX").astype(float) +
        0.2*(channel == "WEB").astype(float)
    )
    prob = 1 / (1 + np.exp(-base_logit))
    y = (rng.uniform(0,1,size=n_samples) < prob).astype(int)

    df = pd.DataFrame({
        "amount": amount,
        "merchant_risk_score": merchant_risk,
        "device_trust_score": device_trust,
        "channel": channel,
        "hour": hour,
        "country": country,
        "user_txn_24h": user_txn_24h,
        "is_fraud": y,
    })
    return df

def train(n_samples: int = 50000):
    df = make_synth(n_samples=n_samples)
    X = df.drop(columns=["is_fraud"])
    y = df["is_fraud"]

    X = pd.get_dummies(X, columns=["channel","country"], drop_first=False)
    feature_names = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)

    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, y_proba)
    print(f"AUC: {auc:.3f}")
    print(classification_report(y_test, (y_proba >= 0.5).astype(int)))

    save_model(model, feature_names)
    print("Modelo salvo em model/model.pkl e feature_names.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-samples", type=int, default=50000)
    args = parser.parse_args()
    train(n_samples=args.n_samples)
