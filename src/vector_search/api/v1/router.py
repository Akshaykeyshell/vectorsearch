from fastapi import APIRouter
from vector_search.api.v1 import search, documents

# Main API router configuration
router = APIRouter()
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(search.router, prefix="/search", tags=["search"])