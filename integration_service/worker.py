"""
Integration Service (ERP Simulator) publisher (Симулятор ERP, що публікує події).
Sends resource updates to RabbitMQ every 5 seconds (Надсилає оновлення ресурсів кожні 5 секунд).
"""

import json
import os
import random
import time

import pika


def create_connection() -> pika.BlockingConnection:
    """Create RabbitMQ connection from env URL (Створити підключення RabbitMQ з URL у змінних середовища)."""
    rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/%2F")
    params = pika.URLParameters(rabbit_url)
    return pika.BlockingConnection(params)


def main() -> None:
    print("Starting Integration Service (ERP Simulator)")
    # Give RabbitMQ time to start (Дати RabbitMQ час запуститися)
    time.sleep(10)

    connection = create_connection()
    channel = connection.channel()

    # Declare exchange (Створити обмінник)
    channel.exchange_declare(exchange="dt4_exchange", exchange_type="topic")

    try:
        while True:
            # Simulate incoming data (Імітація даних з облікової системи)
            data = {
                "type": "Financial",
                "value": round(random.uniform(30.0, 90.0), 2),
            }

            channel.basic_publish(
                exchange="dt4_exchange",
                routing_key="data.accounting.financial",
                body=json.dumps(data),
            )
            print(f"[ERP SIM] Sent update: Financial = {data['value']}")
            time.sleep(5)
    finally:
        try:
            connection.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()






