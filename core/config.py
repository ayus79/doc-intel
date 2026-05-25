from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "doc_intel"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    ollama_host: str = "http://localhost:11434"
    embed_model: str = "nomic-embed-text"
    llm_model: str = "qwen2.5:14b"

    class Config:
        env_file = ".env"


settings = Settings()
