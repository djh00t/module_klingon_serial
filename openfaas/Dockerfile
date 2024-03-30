FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "handler:app", "--host", "0.0.0.0", "--port", "8080"]
