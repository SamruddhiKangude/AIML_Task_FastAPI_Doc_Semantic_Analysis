from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    company_name: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    company_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
