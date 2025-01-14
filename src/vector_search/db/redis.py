from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from vector_search.core.config import settings
from vector_search.core.exceptions import RedisConnectionError

def get_redis_client() -> Redis:
    """Set up and verify Redis connection."""
    client = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True
    )
    try:
        client.ping()
        return client
    except Exception as e:
        raise RedisConnectionError(f"Failed to connect to Redis: {str(e)}")

def create_index(client: Redis) -> None:
    """Create Redis search index for document storage with vector embeddings."""
    schema = (
        TextField("$.content", as_name="content"),
        VectorField(
            "$.embedding",
            "FLAT",
            {
                "TYPE": "FLOAT32",
                "DIM": settings.vector_dim,
                "DISTANCE_METRIC": "COSINE"
            },
            as_name="embedding"
        )
    )
    try:
        client.ft("doc_index").create_index(
            fields=schema,
            definition=IndexDefinition(
                prefix=["doc:"],
                index_type=IndexType.JSON
            )
        )
    except Exception as e:
        if "Index already exists" not in str(e):
            raise