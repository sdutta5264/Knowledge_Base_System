from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    id: int
    age: Optional

    model_config = {
        "from_attributes": True
    }
    # or #Both works same.
    class Config:
        from_attributes = True