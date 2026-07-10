.PHONY: install test evaluate gate reports api dashboard docker

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

test:
	pytest

evaluate:
	python -m llmops_governance.cli evaluate

gate:
	python -m llmops_governance.cli run-gate

reports:
	python -m llmops_governance.cli generate-reports

api:
	uvicorn llmops_governance.api.main:app --reload

dashboard:
	streamlit run app/streamlit_app.py

docker:
	docker compose up --build

