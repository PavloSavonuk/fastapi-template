# Використовуємо офіційний образ Python
FROM python:3.13-slim

# Встановлюємо poetry
RUN pip install poetry

# Встановлюємо робочу директорію
WORKDIR /code

# Копіюємо лише файли конфігурації для встановлення залежностей
COPY pyproject.toml poetry.lock* /code/

# Налаштовуємо poetry: створювати середовище не в окремій папці, 
# а прямо в системі контейнера (це краще для Docker)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копіюємо весь інший код
COPY . /code/

# Команда для запуску з автоперезавантаженням
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]