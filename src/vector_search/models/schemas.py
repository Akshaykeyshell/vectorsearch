from pydantic import BaseModel, Field
from typing import List

class Document(BaseModel):
    content: str
    embedding: List[float]

class SearchQuery(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=100)

class SearchResult(BaseModel):
    content: str
    similarity_score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

class UploadResponse(BaseModel):
    doc_id: str
    num_chunks: int