from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    DB_DRIVER: str = "asyncpg"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DATABASE: str = "postgres"
    ORIGIN: str = "http://localhost:3000"
    SECRET_KEY: str = "your_secret_key"


settings = Settings()
