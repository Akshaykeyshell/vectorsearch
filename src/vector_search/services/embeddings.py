import google.generativeai as genai
from typing import List
from vector_search.core.config import settings
from vector_search.core.exceptions import EmbeddingError

class EmbeddingService:
    """Service for generating text embeddings using Google's Gemini API."""

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = settings.embedding_model

    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for input text using Gemini API."""
        try:
            response = genai.embed_content(
                model=self.model,
                content=text,
                task_type='semantic_similarity'
            )
            return response["embedding"]
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")