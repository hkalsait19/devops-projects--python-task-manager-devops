# Build stage
FROM python:3.12-slim-bullseye AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies separately to preserve the dependency layer cache.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim-bullseye

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Bring installed dependencies from the builder and copy the application.
COPY --from=builder /usr/local /usr/local
COPY app.py .

RUN useradd --create-home appuser
USER appuser

EXPOSE 5151
CMD ["python", "app.py"]