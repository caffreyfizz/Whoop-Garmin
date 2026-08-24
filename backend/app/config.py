from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, sourced from environment variables / .env.

    No secrets have defaults — every credential must come from the
    environment so nothing sensitive is ever committed to the repo.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = "development"
    backend_base_url: str = "http://localhost:8000"

    telegram_bot_token: str = ""

    whoop_client_id: str = ""
    whoop_client_secret: str = ""
    whoop_redirect_uri: str = ""

    oauth_state_secret: str = ""


settings = Settings()
