# app/services/rag_service.py
from app.services.azure_embeddings_service import EmbeddingService
from app.db.elasticsearch import AsyncElasticsearch
from app.core.config import settings
from typing import List, Dict, Any


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.es_client = AsyncElasticsearch()

    async def get_relevant_context(self, query: str) -> List[str]:
        """Get relevant context from vector store."""
        try:
            # Generate embedding for query
            embedding = await self.embedding_service.get_embedding(query)

            # Search in Elasticsearch
            results = await self.es_client.search(
                index=settings.ELASTICSEARCH_INDEX,
                body={
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {"query_vector": embedding}
                            }
                        }
                    },
                    "size": settings.VECTOR_SEARCH_TOP_K
                }
            )

            # Extract and return relevant text passages
            context = [
                hit["_source"]["text"]
                for hit in results["hits"]["hits"]
            ]

            return context

        except Exception as e:
            print(f"Error in get_relevant_context: {str(e)}")
            return []

    async def compute_metadata(self, context: List[str]) -> Dict[str, Any]:
        """Compute metadata about the context (optional)."""
        return {
            "num_passages": len(context),
            "total_length": sum(len(c) for c in context)
        }
