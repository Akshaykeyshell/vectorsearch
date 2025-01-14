class VectorSearchException(Exception):
    """Base exception for vector search operations"""
    pass

class EmbeddingError(VectorSearchException):
    """Raised when embedding generation fails"""
    pass

class RedisConnectionError(VectorSearchException):
    """Raised when Redis connection fails"""
    pass