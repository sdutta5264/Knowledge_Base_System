from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    id: int

    model_config = {
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
