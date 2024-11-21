# app/db/elasticsearch.py
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk
from typing import List, Dict, Any, Generator
import asyncio
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AsyncElasticsearchClient:
    """Async Elasticsearch client for vector search."""

    def __init__(self):
        self.client = AsyncElasticsearch(
            hosts=[{
                'host': settings.ELASTICSEARCH_HOST,
                'port': settings.ELASTICSEARCH_PORT,
                'scheme': 'https'
            }],
            basic_auth=(
                settings.ELASTICSEARCH_USER,
                settings.ELASTICSEARCH_PASSWORD
            ),
            verify_certs=False
        )
        self.index_name = "transport_vectors"
        self.chunk_size = 500

    async def initialize(self):
        """Initialize Elasticsearch with proper mappings."""
        try:
            if not await self.client.indices.exists(index=self.index_name):
                await self.create_index()
        except Exception as e:
            logger.error(f"Error initializing Elasticsearch: {str(e)}")
            raise

    async def create_index(self):
        """Create index with vector search mappings."""
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "refresh_interval": "1s"
        }

        mappings = {
            "properties": {
                "text": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 1536,  # Dimension of text-embedding-3-large
                    "index": True,
                    "similarity": "cosine"
                },
                "metadata": {"type": "object"},
                "timestamp": {"type": "date"}
            }
        }

        await self.client.indices.create(
            index=self.index_name,
            settings=settings,
            mappings=mappings
        )

    def create_documents(
            self,
            texts: List[str],
            embeddings: List[List[float]],
            metadata: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Create documents for bulk indexing."""
        for text, embedding, meta in zip(texts, embeddings, metadata):
            yield {
                "_index": self.index_name,
                "_source": {
                    "text": text,
                    "embedding": embedding,
                    "metadata": meta,
                    "timestamp": "now"
                }
            }

    async def index_documents(
            self,
            texts: List[str],
            embeddings: List[List[float]],
            metadata: List[Dict[str, Any]] = None
    ):
        """Bulk index documents with their embeddings."""
        if metadata is None:
            metadata = [{} for _ in texts]

        try:
            documents = self.create_documents(texts, embeddings, metadata)
            await async_bulk(self.client, documents)
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise

    async def search_similar(
            self,
            query_vector: List[float],
            k: int = 3,
            min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity."""
        try:
            response = await self.client.search(
                index=self.index_name,
                body={
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    "_source": ["text", "metadata"],
                    "size": k,
                    "min_score": min_score
                }
            )

            return [
                {
                    "text": hit["_source"]["text"],
                    "metadata": hit["_source"]["metadata"],
                    "score": hit["_score"]
                }
                for hit in response["hits"]["hits"]
            ]

        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    async def delete_by_query(self, query: Dict[str, Any]):
        """Delete documents matching a query."""
        try:
            await self.client.delete_by_query(
                index=self.index_name,
                body={"query": query}
            )
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise

    async def close(self):
        """Close Elasticsearch connection."""
        await self.client.close()


# Singleton instance
es_client = AsyncElasticsearchClient()


async def init_elasticsearch():
    """Initialize Elasticsearch connection."""
    await es_client.initialize()


async def get_elasticsearch() -> AsyncElasticsearchClient:
    """Dependency injection for FastAPI."""
    return es_client
