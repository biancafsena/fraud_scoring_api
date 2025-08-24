# Fraud Scoring API (FastAPI + scikit‑learn) — Banking/PIX Demo

**Objetivo:** chamar atenção de recrutadores com um projeto **mão‑na‑massa**: um microserviço **FastAPI** que treina e serve um modelo de **fraude em transações** (cartão/PIX), com **Docker**, **tests** e **documentação**.

## O que tem aqui
- `train.py`: gera dados sintéticos de transações e treina um modelo (scikit‑learn).
- `api.py`: serviço FastAPI com `/predict` e `/health`. Tem **OpenAPI** automático.
- `schema.py`: validação Pydantic (payloads)
- `utils.py`: feature engineering e persistência de modelo.
- `tests/`: teste de API com `TestClient`.
- `Dockerfile`: deploy simples com Uvicorn.
- `requirements.txt` e `Makefile` (atalhos).
- **Post pronto** para LinkedIn no final do README.

## Stack
- Python 3.10+
- scikit-learn, pandas, numpy, joblib
- FastAPI, Uvicorn, Pydantic
- Docker (opcional)

---

##  Como rodar local (sem Docker)
Crie e ative o ambiente:
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

1) **Treine o modelo**
```bash
python -m src.train --n-samples 50000
```
Gera `model/model.pkl` e `model/feature_names.json`.

2) **Suba a API**
```bash
uvicorn src.api:app --reload --port 8000
```
Abra: http://127.0.0.1:8000/docs

3) **Teste rápido no terminal**
```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{
  "amount": 325.5,
  "merchant_risk_score": 0.75,
  "device_trust_score": 0.30,
  "channel": "PIX",
  "hour": 2,
  "country": "BR",
  "user_txn_24h": 5
}'
```

---

##  Rodando com Docker
```bash
docker build -t fraud-api:latest .
docker run -p 8000:8000 fraud-api:latest
# docs: http://127.0.0.1:8000/docs
```

---

## Rodando testes
```bash
pytest -q
```

---

## Estrutura
```
fraud_scoring_api/
├─ src/
│  ├─ __init__.py
│  ├─ api.py
│  ├─ schema.py
│  ├─ train.py
│  └─ utils.py
├─ tests/
│  └─ test_api.py
├─ model/  (gerado após treino)
├─ Dockerfile
├─ Makefile
├─ requirements.txt
└─ README.md
```

---

## Ideia do modelo
- Gera **dados sintéticos** com variáveis realistas: `amount`, `merchant_risk_score`, `device_trust_score`, `channel`, `hour`, `country`, `user_txn_24h`.
- Converte categóricas com One‑Hot, normaliza numéricas e treina um **GradientBoostingClassifier**.
- Retorna `fraud_probability` (0–1) + `is_fraud` (limiar padrão 0.5).

---

## Exemplo de payload
```json
{
  "amount": 325.5,
  "merchant_risk_score": 0.75,
  "device_trust_score": 0.30,
  "channel": "PIX",
  "hour": 2,
  "country": "BR",
  "user_txn_24h": 5
}
```


