from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vector_search.core.config import settings
from vector_search.services.embeddings import EmbeddingService
from vector_search.db.redis import get_redis_client
from vector_search.models.schemas import UploadResponse

router = APIRouter()
embedding_service = EmbeddingService()
redis_client = get_redis_client()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap
):
    """Process and store document with vector embeddings.
    
    Splits document into chunks, generates embeddings, and stores in Redis.
    
    input: .txt file,  can be extended to other type easily

    """
    try:
        content = await file.read()
        text_content = content.decode("utf-8")

        # Split text into overlapping chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        chunks = text_splitter.split_text(text_content)

        # Clean up existing chunks if document was previously uploaded
        base_doc_id = f"doc:{file.filename}"
        existing_keys = redis_client.keys(f"{base_doc_id}:chunk:*")
        if existing_keys:
            redis_client.delete(*existing_keys)

        # Process and store each chunk with its embedding
        for i, chunk in enumerate(chunks):
            embedding = await embedding_service.get_embedding(chunk)
            chunk_id = f"{base_doc_id}:chunk:{i}"
            chunk_data = {
                "content": chunk,
                "embedding": embedding
            }
            redis_client.json().set(chunk_id, "$", chunk_data)

        return UploadResponse(
            doc_id=base_doc_id,
            num_chunks=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))