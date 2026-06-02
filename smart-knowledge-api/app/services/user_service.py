from sqlalchemy.orm import session
from app.schema.user import UserCreate, UserResponse
from app.models.user import User
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
from typing import List
from pydantic import EmailStr


def create_user(db: session, user: UserCreate) -> UserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail= "Email Already registered")

    db_user = User(
        email = user.email,
        hashed_password = hash_password(user.password),
        name  = user.name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)

def get_users(db: session) -> List[UserResponse]:
    users = db.query(User).all()
    print(users)
    return [UserResponse.model_validate(user) for user in users]

def login_user(db: session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code= 401, detail = "Invalid Credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code= 401, detail = "Invalid Credentials")

    token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token" : token,
        "token_type": "bearer"
    }