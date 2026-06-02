from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.database import Base
from app.db.database import engine

class Note(Base):
    __tablename__ = "notes_knowledge_db"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

# Base.metadata.create_all(bind=engine)