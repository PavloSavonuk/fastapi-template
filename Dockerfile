FROM python:3.13-slim

WORKDIR /code

# 1. Копіюємо файл залежностей
COPY pyproject.toml /code/

# 2. Встановлюємо залежності з pyproject.toml
# Ми використовуємо крапку (.), щоб pip встановив все, що описано у файлі
RUN pip install --no-cache-dir .

# 3. Копіюємо решту коду
COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]