from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, List
from pydantic import Field, AliasChoices
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENAI_API_KEY: str | None = None
    DATABASE_URL: str = "sqlite:///./fa.db"  # Temp: SQLite for local POC
    # Store as raw string (CSV or JSON) to avoid pydantic env JSON decoding issues
    ALLOW_ORIGINS_RAW: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        validation_alias=AliasChoices("ALLOW_ORIGINS", "ALLOW_ORIGINS_RAW"),
    )
    BASE_CURRENCY: str = "EUR"
    JWT_SECRET: str = "change_me_dev_secret"
    JWT_ALGO: str = "HS256"
    CASH_MIN_THRESHOLD: float = 1000.0

    def allow_origins(self) -> List[str]:
        v = (self.ALLOW_ORIGINS_RAW or "").strip()
        if not v:
            return []
        if v.startswith("["):
            try:
                arr = json.loads(v)
                return [str(x) for x in arr]
            except Exception:
                pass
        return [s.strip() for s in v.split(",") if s.strip()]

settings = Settings()
