# Указываем базовый образ Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости для PostgreSQL и других пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Создаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock (если есть)
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальной код
COPY . /app

# Указываем команду запуска (можно изменить по необходимости)
CMD ["poetry", "run", "python", "-m", "src.bot.bot"]
