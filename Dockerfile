FROM python:3.11-slim

# Set workdir (Робоча директорія)
WORKDIR /code

# Install system deps if needed (за потреби можна додати системні залежності)

# Copy requirements and install (Скопіювати залежності та встановити)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (Скопіювати код застосунку)
COPY . .

# Default command can be overridden by Compose/Render (Команда за замовчуванням змінюється Compose/Render)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]






