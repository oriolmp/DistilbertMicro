# ---------- Base image ----------
FROM python:3.12-slim AS base

# Set env vars
ENV POETRY_VERSION=2.1.3 
ENV HOST="0.0.0.0"

# ---------- Install poetry ----------
FROM base AS poetry-install

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION" && mkdir .p /app
COPY . /app

WORKDIR /app

# Install dependencies
RUN poetry install

# Expose port
EXPOSE 8000

# Start app
CMD ["poetry", "run", "uvicorn", "src.entrypoints.cli:app", "--host", "0.0.0.0", "--reload"]
