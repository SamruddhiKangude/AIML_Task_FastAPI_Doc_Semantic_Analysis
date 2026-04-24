from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    documents = relationship("Document", back_populates="uploader")
