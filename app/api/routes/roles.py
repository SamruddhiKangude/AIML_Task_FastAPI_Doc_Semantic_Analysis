from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.deps import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.role import PermissionOut, RoleAssign, RoleCreate, RoleOut
from app.services.rbac import ROLE_PERMISSIONS, get_permissions_for_roles

router = APIRouter(tags=["Roles"])


@router.post("/roles/create", response_model=RoleOut)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(["Admin"])),
):
    role = db.query(Role).filter(Role.name == payload.name).first()
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(name=payload.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.post("/users/assign-role")
def assign_role(
    payload: RoleAssign,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(["Admin"])),
):
    user = db.query(User).filter(User.id == payload.user_id).first()
    role = db.query(Role).filter(Role.name == payload.role_name).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role not in user.roles:
        user.roles.append(role)
        db.commit()

    return {"message": f"Role '{role.name}' assigned to user {user.email}"}


@router.get("/users/{id}/roles", response_model=list[RoleOut])
def get_user_roles(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin = any(role.name == "Admin" for role in current_user.roles)
    if not is_admin and current_user.id != id:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.roles


@router.get("/users/{id}/permissions", response_model=list[PermissionOut])
def get_user_permissions(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin = any(role.name == "Admin" for role in current_user.roles)
    if not is_admin and current_user.id != id:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_names = [role.name for role in user.roles]
    computed_permissions = get_permissions_for_roles(role_names)

    response: list[PermissionOut] = []
    for role_name in role_names:
        perms = ROLE_PERMISSIONS.get(role_name, [])
        response.append(PermissionOut(role=role_name, permissions=perms))

    if computed_permissions and "*" in computed_permissions and all(item.role != "Admin" for item in response):
        response.append(PermissionOut(role="Admin", permissions=["*"]))

    return response
