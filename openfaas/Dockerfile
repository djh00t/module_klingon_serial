FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY handler.py .

CMD ["uvicorn", "handler:app", "--host", "0.0.0.0", "--port", "8080"]
