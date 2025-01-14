from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    redis_host: str = "localhost"
    redis_port: int = 6379
    gemini_api_key: str
    embedding_model: str = "models/text-embedding-004"
    vector_dim: int = 768  # Dimension of the embedding vectors
    chunk_size: int = 750  # Size of text chunks for processing
    chunk_overlap: int = 200  # Overlap between consecutive chunks

    class Config:
        env_file = ".env"

settings = Settings()