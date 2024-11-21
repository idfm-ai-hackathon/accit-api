# app/utils/helpers.py
from typing import List, Dict, Any
import numpy as np


def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return np.dot(v1, v2) / (norm1 * norm2)


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)

    return chunks


# Add to app/api/routes/transport.py
from app.db.elasticsearch import get_elasticsearch
from app.services.embedding_service import EmbeddingService
from fastapi import Depends


@router.post("/index-documents")
async def index_documents(
        texts: List[str],
        metadata: List[Dict[str, Any]] = None,
        es_client: AsyncElasticsearchClient = Depends(get_elasticsearch),
        embedding_service: EmbeddingService = Depends()
):
    """Index new documents with their embeddings."""
    try:
        # Generate embeddings
        embeddings = await embedding_service.get_embeddings(texts)

        # Index documents
        await es_client.index_documents(
            texts=texts,
            embeddings=embeddings,
            metadata=metadata
        )

        return {"status": "success", "count": len(texts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
