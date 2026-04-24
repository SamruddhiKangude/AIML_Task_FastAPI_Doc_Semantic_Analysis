from pydantic import BaseModel


class IndexDocumentRequest(BaseModel):
    document_id: int


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    document_id: int
    chunk_id: int
    score: float
    rerank_score: float
    title: str
    company_name: str
    document_type: str
    text: str
