"""
RabbitMQ consumer for dt4research (Слухач RabbitMQ для dt4research).
Consumes data updates and persists them via repository (Отримує оновлення та зберігає через репозиторій).
"""

import json
import os
import time
from typing import Any

import pika

from app.models import ResourceType
from app.repository import read_system_state, write_system_state


def get_rabbit_params() -> pika.URLParameters:
    """Build pika URL parameters from env (Побудувати параметри pika з оточення)."""
    rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/%2F")
    return pika.URLParameters(rabbit_url)


def update_resource_value(resource_type: ResourceType, new_value: float) -> None:
    """Update specific resource value using repository (Оновити значення ресурсу через репозиторій)."""
    try:
        current_state = read_system_state()
        updated = False
        for resource in current_state.resources:
            if resource.type == resource_type:
                resource.value = new_value
                updated = True
                break

        if updated:
            write_system_state(current_state)
            print(f"[Consumer] Updated DB: {resource_type.value} = {new_value}")
        else:
            print(f"[Consumer] Error: Resource type '{resource_type.value}' not found in state.")
    except Exception as exc:
        print(f"[Consumer] Error updating database: {exc}")


def callback(ch: Any, method: Any, properties: Any, body: bytes) -> None:
    """Process incoming message (Обробити вхідне повідомлення)."""
    print(f"[Consumer] Received message: {body.decode()}")
    try:
        data = json.loads(body.decode())
        if "type" in data and "value" in data:
            resource_type = ResourceType(str(data["type"]))
            new_value = float(data["value"])
            update_resource_value(resource_type, new_value)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f"[Consumer] Error processing message: {exc}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main() -> None:
    print("Starting API Consumer")
    # Give RabbitMQ time to start (Дати RabbitMQ час запуститися)
    time.sleep(10)

    connection = pika.BlockingConnection(get_rabbit_params())
    channel = connection.channel()

    channel.exchange_declare(exchange="dt4_exchange", exchange_type="topic")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="dt4_exchange", queue=queue_name, routing_key="data.#")

    print("[Consumer] Waiting for data updates. To exit press CTRL+C")
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    main()






