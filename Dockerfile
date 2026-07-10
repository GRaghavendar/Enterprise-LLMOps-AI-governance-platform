FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY requirements.txt pyproject.toml README.md ./
COPY src ./src
COPY app ./app
COPY data ./data
COPY knowledge_base ./knowledge_base

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -e .

EXPOSE 8000 8501

CMD ["python", "-m", "llmops_governance.cli", "serve-api"]

