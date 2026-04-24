from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.deps import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.rag import IndexDocumentRequest, SearchRequest
from app.services.rag_service import rag_service

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/index-document")
def index_document(
    payload: IndexDocumentRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(["Admin", "Financial Analyst"])),
):
    document = db.query(Document).filter(Document.id == payload.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not document.content_text:
        raise HTTPException(status_code=400, detail="Document has no extracted text")

    count = rag_service.index_document(
        document_id=document.id,
        text=document.content_text,
        title=document.title,
        company_name=document.company_name,
        document_type=document.document_type,
    )
    return {"message": "Document indexed", "chunks_indexed": count}


@router.delete("/remove-document/{id}")
def remove_document(
    id: int,
    _: User = Depends(require_roles(["Admin", "Financial Analyst"])),
):
    rag_service.remove_document(id)
    return {"message": "Document embeddings removed"}


@router.post("/search")
def semantic_search(
    payload: SearchRequest,
    current_user: User = Depends(get_current_user),
):
    role_names = {role.name for role in current_user.roles}
    company_filter = current_user.company_name if "Client" in role_names else None

    results = rag_service.search(query=payload.query, limit=payload.limit, company_name=company_filter)
    return {"query": payload.query, "results": results}


@router.get("/context/{document_id}")
def get_context(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    role_names = {role.name for role in current_user.roles}
    if "Client" in role_names and current_user.company_name != document.company_name:
        raise HTTPException(status_code=403, detail="Forbidden")

    context = rag_service.context_for_document(document_id)
    return {"document_id": document_id, "context": context}
