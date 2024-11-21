# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "IDFM Accessibility Assistant"
    API_V1_STR: str = "/api/v1"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]

    # Azure OpenAI settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

    # Elasticsearch settings
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "elastic-319059-elasticsearch")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_USERNAME: str = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD", "")

    # S3/MinIO settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_SESSION_TOKEN: str = os.getenv("AWS_SESSION_TOKEN", "")
    AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION", "fr-central")
    AWS_S3_ENDPOINT: str = os.getenv("AWS_S3_ENDPOINT", "minio.data-platform-self-service.net")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "dlb-hackathon")

    # Vector search settings
    VECTOR_SEARCH_TOP_K: int = 3
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # IDFM API settings
    IDFM_API_KEY: str = os.getenv("IDFM_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # This allows extra fields


settings = Settings()
