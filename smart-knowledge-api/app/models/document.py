from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents_knowledge_db"

    id = Column(Integer, primary_key = True, index = True)
    filename = Column(String, nullable= False)
    content = Column(Text, nullable= False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"))