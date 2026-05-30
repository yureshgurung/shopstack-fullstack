#=========================
# 1. Builder Stage
# =========================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (IMPORTANT for MySQL + builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .


# Virtual environment
RUN python -m venv /venv && \
     /venv/bin/pip install --upgrade pip setuptools wheel && \
    /venv/bin/pip install --no-cache-dir --force-reinstall setuptools && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt
#RUN python -m venv /venv && \
    #/venv/bin/pip install --upgrade pip && \
    #/venv/bin/pip install --no-cache-dir -r requirements.txt


# =========================
# 2. Runtime Stage
# =========================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy venv
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]