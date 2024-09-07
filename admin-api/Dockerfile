FROM python:3.10-slim

WORKDIR /app

COPY admin-api/poetry.lock admin-api/pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry

COPY admin-api ./

RUN poetry install --no-root

RUN poetry show 

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
