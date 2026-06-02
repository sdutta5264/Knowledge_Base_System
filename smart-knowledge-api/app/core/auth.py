from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import session
from app.db.dependencies import get_db
from app.models.user import User

ouath2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(ouath2_schema), db: session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user