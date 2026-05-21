from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"
    POSTGRES_DB: str = "fastapi_db"
    
    # Залишаємо None, щоб автоматично збирати правильний URL для Docker
    DATABASE_URL: str | None = None

    @property
    def get_db_url(self) -> str:
        # Для Docker збираємо асинхронний URL через назву сервісу бази 'db'
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:5432/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()