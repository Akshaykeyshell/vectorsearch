from fastapi import APIRouter, HTTPException
from redis.commands.search.query import Query
import numpy as np
from vector_search.models.schemas import SearchQuery, SearchResponse, SearchResult
from vector_search.services.embeddings import EmbeddingService
from vector_search.db.redis import get_redis_client

router = APIRouter()
embedding_service = EmbeddingService()
redis_client = get_redis_client()

@router.post("/", response_model=SearchResponse)
async def search_documents(query: SearchQuery):
    """Search for similar documents using vector similarity."""
    try:
        # Generate embedding for search query
        embedding = await embedding_service.get_embedding(query.query)
        query_vector = np.array(embedding, dtype=np.float32).tobytes()

        # Construct Redis vector similarity search query
        redis_query = (
            Query("(*)=>[KNN $K @embedding $query_vector AS vector_score]")
            .sort_by("vector_score")
            .dialect(2)
            .return_fields("content", "vector_score")
        )

        # Execute search and format results
        results = redis_client.ft("doc_index").search(
            redis_query,
            {"query_vector": query_vector, "K": query.top_k}
        )
        search_results = [
            SearchResult(
                content=doc.content,
                similarity_score=1 - float(doc.vector_score) if hasattr(doc, 'vector_score') else 0.0
            )
            for doc in results.docs
        ]
        
        return SearchResponse(results=search_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))