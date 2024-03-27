FROM python:3.8-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers build-base libffi-dev


RUN pip install --no-cache-dir Cython

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY handler.py .

CMD ["uvicorn", "handler:app", "--host", "0.0.0.0", "--port", "8080"]
