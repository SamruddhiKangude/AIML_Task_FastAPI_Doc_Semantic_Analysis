from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams
from sentence_transformers import CrossEncoder, SentenceTransformer

from app.core.config import settings


class RagService:
    def __init__(self) -> None:
        self.embedder = SentenceTransformer(settings.embedding_model_name)
        self.reranker = CrossEncoder(settings.reranker_model_name)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=120,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self.client = self._build_qdrant_client()
        self._ensure_collection()

    def _build_qdrant_client(self) -> QdrantClient:
        try:
            return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        except Exception:
            return QdrantClient(path=":memory:")

    def _switch_to_embedded_qdrant(self) -> None:
        # Remote Qdrant is optional for local development.
        self.client = QdrantClient(path=":memory:")

    def _ensure_collection(self) -> None:
        try:
            collections = self.client.get_collections().collections
        except Exception:
            self._switch_to_embedded_qdrant()
            collections = self.client.get_collections().collections

        collection_names = {collection.name for collection in collections}

        if settings.qdrant_collection not in collection_names:
            self.client.create_collection(
                collection_name=settings.qdrant_collection,
                vectors_config=VectorParams(size=settings.embedding_vector_size, distance=Distance.COSINE),
            )

    def index_document(
        self,
        document_id: int,
        text: str,
        title: str,
        company_name: str,
        document_type: str,
    ) -> int:
        chunks = self.splitter.split_text(text)
        if not chunks:
            return 0

        vectors = self.embedder.encode(chunks, normalize_embeddings=True)
        points: list[PointStruct] = []

        for idx, chunk in enumerate(chunks):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vectors[idx].tolist(),
                    payload={
                        "document_id": document_id,
                        "chunk_id": idx,
                        "title": title,
                        "company_name": company_name,
                        "document_type": document_type,
                        "text": chunk,
                    },
                )
            )

        self.client.upsert(collection_name=settings.qdrant_collection, points=points)
        return len(points)

    def remove_document(self, document_id: int) -> None:
        self.client.delete(
            collection_name=settings.qdrant_collection,
            points_selector=Filter(
                must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
            ),
        )

    def search(self, query: str, limit: int = 5, company_name: str | None = None) -> list[dict]:
        vector = self.embedder.encode(query, normalize_embeddings=True).tolist()

        query_filter = None
        if company_name:
            query_filter = Filter(
                must=[FieldCondition(key="company_name", match=MatchValue(value=company_name))]
            )

        candidates = self.client.query_points(
            collection_name=settings.qdrant_collection,
            query=vector,
            query_filter=query_filter,
            limit=20,
            with_payload=True,
        ).points

        if not candidates:
            return []

        candidate_texts = [point.payload.get("text", "") for point in candidates]
        rerank_inputs = [(query, text) for text in candidate_texts]
        rerank_scores = self.reranker.predict(rerank_inputs).tolist()

        reranked = []
        for point, rerank_score in zip(candidates, rerank_scores, strict=True):
            payload = point.payload
            reranked.append(
                {
                    "document_id": payload.get("document_id"),
                    "chunk_id": payload.get("chunk_id"),
                    "score": float(point.score),
                    "rerank_score": float(rerank_score),
                    "title": payload.get("title"),
                    "company_name": payload.get("company_name"),
                    "document_type": payload.get("document_type"),
                    "text": payload.get("text"),
                }
            )

        reranked.sort(key=lambda item: item["rerank_score"], reverse=True)
        return reranked[:limit]

    def context_for_document(self, document_id: int, limit: int = 10) -> list[dict]:
        points, _ = self.client.scroll(
            collection_name=settings.qdrant_collection,
            scroll_filter=Filter(
                must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
            ),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return [point.payload for point in points]


rag_service = RagService()
