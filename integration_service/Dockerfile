FROM python:3.11-slim

WORKDIR /code

# Install runtime dependency (Встановити залежність рантайму)
RUN pip install --no-cache-dir pika==1.3.2

COPY . .

CMD ["python", "worker.py"]






