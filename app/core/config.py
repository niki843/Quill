from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Quill API"
    database_url: str = "postgresql+asyncpg://postgresql:postgresql@db:5432/postgresql"


settings = Settings()
