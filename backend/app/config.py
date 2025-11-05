from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/financial_assistant"
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_GPT4: str = "gpt-4-turbo-preview"
    OPENAI_MODEL_GPT35: str = "gpt-3.5-turbo"
    OPENAI_MODEL_VISION: str = "gpt-4-vision-preview"
    
    # Storage
    STORAGE_PATH: str = "./storage"
    INVOICE_PATH: str = "./storage/invoices"
    REPORT_PATH: str = "./storage/reports"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Agent settings
    AGENT_VERBOSE: bool = True
    AGENT_MAX_ITERATIONS: int = 5
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()