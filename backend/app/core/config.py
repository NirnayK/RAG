from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    # Database settings
    DB_DRIVER: str = "asyncpg"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DATABASE: str = "postgres"

    # CORS settings
    ORIGIN: str = "http://localhost:3000"

    # JWT settings
    SECRET_KEY: str = "your_secret_key"
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Logging settings
    LOG_LEVEL: str = "DEBUG"
    ENABLE_LOADAVG: bool = True

    # Vault settings
    VAULT_ADDR: str = "http://127.0.0.1:8200"
    VAULT_TOKEN: str = "your_vault_token"
    VAULT_KV_MOUNT_PATH: str = "secret"


settings = Settings()
