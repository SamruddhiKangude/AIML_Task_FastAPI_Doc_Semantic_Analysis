from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str


class RoleAssign(BaseModel):
    user_id: int
    role_name: str


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PermissionOut(BaseModel):
    role: str
    permissions: list[str]
