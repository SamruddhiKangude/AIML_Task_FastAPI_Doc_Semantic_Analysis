from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Financial Document Management API"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./finance_docs.db"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "financial_documents"

    embedding_model_name: str = "BAAI/bge-base-en-v1.5"
    reranker_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    embedding_vector_size: int = 768

    document_storage_path: str = "storage/documents"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
