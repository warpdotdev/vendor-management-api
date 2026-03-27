from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vendor Management API"
    database_url: str = "sqlite:///./vendor_management.db"
    secret_key: str = "CHANGE-ME-IN-PRODUCTION"
    access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env"}


settings = Settings()
