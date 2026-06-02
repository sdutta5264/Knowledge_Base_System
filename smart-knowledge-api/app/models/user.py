from sqlalchemy import Column, Integer, String
from app.db.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable= False)
    name = Column(String, nullable= False)

# Base.metadata.create_all(bind=engine)