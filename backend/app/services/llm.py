from openai import OpenAI
from ..core.config import settings

_client: OpenAI | None = None

def get_openai() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY non configurée. Ajoutez-la dans .env")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client
