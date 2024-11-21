# app/services/embedding_service.py
from langchain_openai import AzureOpenAIEmbeddings
from typing import List
import numpy as np
from app.core.config import settings
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential


class EmbeddingService:
    """Service for generating embeddings using Azure OpenAI."""

    def __init__(self):
        self.embedding_model = AzureOpenAIEmbeddings(
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            model="text-embedding-3-large",
            chunk_size=settings.CHUNK_SIZE,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(Exception)
    )
    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            embedding = await self.embedding_model.aembed_query(text)
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(Exception)
    )
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            embeddings = await self.embedding_model.aembed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise

    def normalize_embedding(self, embedding: List[float]) -> List[float]:
        """Normalize embedding vector to unit length."""
        norm = np.linalg.norm(embedding)
        if norm > 0:
            return [x / norm for x in embedding]
        return embedding
