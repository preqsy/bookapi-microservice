FROM python:3.10-slim

WORKDIR /app

COPY frontend-api/poetry.lock frontend-api/pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry

COPY frontend-api ./

RUN poetry install --no-root

RUN poetry show 

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
