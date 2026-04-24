from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: int
    title: str
    company_name: str
    document_type: str
    uploaded_by: int
    created_at: datetime


class DocumentSearchQuery(BaseModel):
    title: str | None = None
    company_name: str | None = None
    document_type: str | None = None
    uploaded_by: int | None = None
