from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import user_roles


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")
