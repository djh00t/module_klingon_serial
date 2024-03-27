FROM python:alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers build-base libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

CMD ["uvicorn", "handler:app", "--host", "0.0.0.0", "--port", "8080"]
