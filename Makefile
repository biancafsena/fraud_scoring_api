# Makefile
.PHONY: venv install train run test docker

venv:
	python -m venv .venv

install:
	. .venv/bin/activate || .venv\Scripts\activate && pip install -r requirements.txt

train:
	python -m src.train --n-samples 50000

run:
	uvicorn src.api:app --reload --port 8000

test:
	pytest -q

docker:
	docker build -t fraud-api:latest . && docker run -p 8000:8000 fraud-api:latest
