from contextlib import asynccontextmanager
from fastapi import FastAPI
from vector_search.api.v1.router import router as api_v1_router
from vector_search.db.redis import create_index, get_redis_client

# This ensures that the Redis search index is created when the application starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_index(get_redis_client())
    yield

# Create the FastAPI application instance with metadata and lifespan management
app = FastAPI(
    title="Document Search Service",
    description="Vector search service using Redis and Gemini AI",
    version="1.0.0",
    lifespan=lifespan
)

# Include the API router
app.include_router(api_v1_router, prefix="/api/v1")