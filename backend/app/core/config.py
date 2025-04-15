from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    pass


settings = Settings()
