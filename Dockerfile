# Dockerfile
FROM python:3.12-slim

WORKDIR /app
RUN mkdir -p /app/logs

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY datenoapi /app/datenoapi
COPY run_mcp.py /app/run_mcp.py

EXPOSE 8100

CMD ["sh", "-c", "hypercorn -b 0.0.0.0:8100 datenoapi.app:app > logs/api-public.log 2>&1"]