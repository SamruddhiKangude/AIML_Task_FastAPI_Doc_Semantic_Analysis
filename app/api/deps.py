from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.deps import get_db
from app.models.user import User
from app.services.rbac import get_permissions_for_roles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        role_names = [role.name for role in current_user.roles]
        if not any(role in allowed_roles for role in role_names):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return role_checker


def require_permission(permission: str):
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        role_names = [role.name for role in current_user.roles]
        permissions = get_permissions_for_roles(role_names)
        if "*" in permissions or permission in permissions:
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permission")

    return permission_checker
