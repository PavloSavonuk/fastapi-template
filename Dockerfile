FROM python:3.13-slim
WORKDIR /code
COPY pyproject.toml /code/
RUN pip install --no-cache-dir fastapi uvicorn email-validator sqlalchemy asyncpg alembic pydantic-settings
COPY . /code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]