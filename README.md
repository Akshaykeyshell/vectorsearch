# Vector Search Service

A FastAPI-based document search service using Redis Vector Search and Gemini AI embeddings.

## Features

- Document upload and chunking
- Vector similarity search
- Redis Vector Database integration
- Gemini AI embeddings
- Asynchronous API endpoints

## Tech Stack

- FastAPI
- Redis Stack (with RediSearch module)
- Gemini AI for embeddings
- Langchain for text processing
- Docker & Docker Compose

## Prerequisites

- Python 3.11+
- Redis Stack Server
- Gemini AI API key

## Installation

# no need if you'v folder
1. Clone the repository:
```bash
git clone <repository-url>
cd vector-search
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:

For development
```bash
pip install -e .
```

For production
```bash
pip install .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Required environment variables in `.env`:
```
REDIS_HOST=localhost
REDIS_PORT=6379
GEMINI_API_KEY=your_api_key_here
```

## Running the Service

### Local Development
```bash
uvicorn src.vector_search.main:app --reload
```

### Using Docker
```bash
docker-compose up --build
```

## API Endpoints

### Upload Document
```http
POST /api/v1/documents/upload
```
Uploads and processes a document for vector search.

**Request:**
- `file`: Document file (multipart/form-data)
- `chunk_size`: (optional) Size of text chunks (default: 750)
- `chunk_overlap`: (optional) Overlap between chunks (default: 200)

**Response:**
```json
{
    "doc_id": "doc:filename.txt",
    "num_chunks": 5
}
```

### Search Documents
```http
POST /api/v1/search
```
Performs semantic search across uploaded documents.

**Request:**
```json
{
    "query": "your search query",
    "top_k": 5
}
```

**Response:**
```json
{
    "results": [
        {
            "content": "matching text chunk",
            "similarity_score": 0.85
        }
    ]
}
```

## Design Decisions

### Redis Implementation
- Using Redis Stack for vector search capabilities
- JSON storage format for flexible document structure
- Vector similarity search using HNSW algorithm
- Cosine similarity metric for better semantic matching

### Text Processing
- Document chunking with overlap for context preservation
- Langchain's RecursiveCharacterTextSplitter for intelligent text splitting
- Chunk size of 750 characters balancing context and precision

### Vector Search
- Gemini AI embeddings (768 dimensions)
- KNN search with cosine similarity
- Configurable top-k results


