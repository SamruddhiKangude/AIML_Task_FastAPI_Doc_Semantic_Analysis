from sqlalchemy.orm import Session

from app.models.role import Role

DEFAULT_ROLES = ["Admin", "Financial Analyst", "Auditor", "Client"]


def seed_roles(db: Session) -> None:
    for role_name in DEFAULT_ROLES:
        exists = db.query(Role).filter(Role.name == role_name).first()
        if not exists:
            db.add(Role(name=role_name))
    db.commit()
