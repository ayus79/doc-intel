import ollama
from core.config import settings

_client = ollama.Client(host=settings.ollama_host)

# Fetch dim dynamically so changing EMBED_MODEL in .env always works
VECTOR_DIM = len(
    _client.embed(model=settings.embed_model, input=["test"]).embeddings[0]
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = _client.embed(model=settings.embed_model, input=texts)
    return response.embeddings


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
