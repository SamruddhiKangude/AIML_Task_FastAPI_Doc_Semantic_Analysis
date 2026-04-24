from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=False, index=True)
    document_type = Column(String, nullable=False, index=True)
    file_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    content_text = Column(Text, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    uploader = relationship("User", back_populates="documents")

    @property
    def document_id(self) -> int:
        return self.id
