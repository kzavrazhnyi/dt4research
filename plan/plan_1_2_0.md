# Етап 3: Інтеграція з реальними даними (Docker + Render)

## Рекомендації

- **Локально (тест)**: Docker Compose з 4 сервісами (`api`, `rabbitmq`, `integration_service`, `api_consumer`). Зберігання — **SQLite файл** (спільний named volume) через існуючий репозиторій.
- **Render (прод)**: 
  - База — **Render Postgres** (`DATABASE_URL`).
  - RabbitMQ — **CloudAMQP (free plan)**, один `RABBITMQ_URL` у `api` і `worker`.
  - Два сервіси з одного репозиторію: **Web (api)** та **Background Worker (api_consumer)**. `integration_service` опційний для демо або виключається на проді.
- **Uvicorn у контейнері** — ок для Docker/Render. Локальні PowerShell-скрипти залишаються для non-Docker запусків.

## Файли/зміни

- Новий `docker-compose.yml` (корінь): 4 сервіси + named volume `db_data`.
- `requirements.txt`: додати `pika==1.3.2` (і, за потреби, `sqlmodel`/`sqlite` якщо ще не додані).
- Новий `integration_service/`:
  - `integration_service/worker.py` — публікує повідомлення кожні 5 с.
  - `integration_service/Dockerfile` — мінімальний образ Python + pika.
- Новий `app/consumer.py` — підписка на `dt4_exchange` (`topic`, ключ `data.#`), виклик `repository.write_system_state()`.
- Root `Dockerfile` для `api` (якщо нема): інсталює залежності, стартує uvicorn `app.main:app`.
- Конфіг через ENV:
  - `RABBITMQ_URL` (за замовчуванням локально `amqp://guest:guest@rabbitmq:5672/%2F`).
  - `DATABASE_URL` (локально `sqlite:///data/data.db`; на Render — Postgres URL).
- Репозиторій/моделі: переконатися, що `read_system_state` / `write_system_state` працюють з поточним шаром збереження. Для локального SQLite — файл у `data/`, змонтований у `db_data`.

## Ключові уривки (нетривіальні)

- Підключення pika через URL (щоб легко переключити RabbitMQ):
```python
import os, pika
from urllib.parse import urlparse

rabbit_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/%2F')
params = pika.URLParameters(rabbit_url)
connection = pika.BlockingConnection(params)
```

- SQLModel `DATABASE_URL` через ENV, з fallback на SQLite для Compose.

## Локальний запуск (Docker Compose)

- Команда: `docker-compose up --build`
- Очікуваний результат: `integration_service` шле `{"type":"Financial","value":..}`; `api_consumer` оновлює стан; UI на `http://localhost:8000` що 5 с опитує `/api/v1/system-state` і бачить зміни.

## Деплой на Render

1. Створити **Render Postgres**, взяти `DATABASE_URL`.
2. Підписатися на **CloudAMQP** (free), взяти `RABBITMQ_URL`.
3. Створити **Web Service (api)**:

   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - ENV: `DATABASE_URL`, `RABBITMQ_URL`, `PYTHONUNBUFFERED=1`

4. Створити **Background Worker (api_consumer)** з того ж репозиторію:

   - Build як вище
   - Start: `python app/consumer.py`
   - ENV: ті самі (`DATABASE_URL`, `RABBITMQ_URL`, `PYTHONUNBUFFERED`)

5. (Опційно) Окремий приватний сервіс для `integration_service` для демо або відключити на проді.

## Примітки сумісності

- Windows non-Docker: як і раніше використовувати `start_server.ps1` для локальних запусків без Compose.
- Файлова БД у продакшні не спільна між сервісами — тому **на Render лише Postgres**.
- Черги/обмінник: `exchange=dt4_exchange`, `type=topic`, `routing_key` з префіксом `data.`.