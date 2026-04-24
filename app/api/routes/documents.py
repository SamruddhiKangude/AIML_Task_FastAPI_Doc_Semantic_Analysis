from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.deps import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentOut
from app.services.text_processing import extract_text
from app.core.config import settings

router = APIRouter(prefix="/documents", tags=["Documents"])

ALLOWED_DOC_TYPES = {"invoice", "report", "contract"}


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin", "Financial Analyst"])),
):
    if document_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(status_code=400, detail=f"document_type must be one of {sorted(ALLOWED_DOC_TYPES)}")

    storage_dir = Path(settings.document_storage_path)
    storage_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix
    file_name = f"{uuid4()}{extension}"
    destination = storage_dir / file_name

    content = await file.read()
    destination.write_bytes(content)

    extracted_text = extract_text(str(destination))

    document = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        file_path=str(destination),
        original_filename=file.filename,
        content_text=extracted_text,
        uploaded_by=current_user.id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get("", response_model=list[DocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document)

    role_names = {role.name for role in current_user.roles}
    if "Client" in role_names:
        if not current_user.company_name:
            return []
        query = query.filter(Document.company_name == current_user.company_name)

    return query.order_by(Document.created_at.desc()).all()


@router.get("/search", response_model=list[DocumentOut])
def search_documents(
    document_id: int | None = None,
    title: str | None = None,
    company_name: str | None = None,
    document_type: str | None = None,
    uploaded_by: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document)

    if document_id:
        query = query.filter(Document.id == document_id)
    if title:
        query = query.filter(Document.title.ilike(f"%{title}%"))
    if company_name:
        query = query.filter(Document.company_name.ilike(f"%{company_name}%"))
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if uploaded_by:
        query = query.filter(Document.uploaded_by == uploaded_by)

    role_names = {role.name for role in current_user.roles}
    if "Client" in role_names:
        if not current_user.company_name:
            return []
        query = query.filter(Document.company_name == current_user.company_name)

    return query.order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    role_names = {role.name for role in current_user.roles}
    if "Client" in role_names and document.company_name != current_user.company_name:
        raise HTTPException(status_code=403, detail="Forbidden")

    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin", "Financial Analyst"])),
):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
    return {"message": "Document deleted"}
