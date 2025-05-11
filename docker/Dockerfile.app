FROM python:3.12-slim-bullseye AS builder

WORKDIR /app

COPY ml/checkpoints/ ml/checkpoints/
COPY src/ src/
COPY .env README.md pyproject.toml poetry.lock .

RUN python -m pip install poetry==1.8.4 \
    && poetry config virtualenvs.in-project true \
    && poetry install

FROM python:3.12-slim-bullseye
COPY --from=builder /app /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4242"]