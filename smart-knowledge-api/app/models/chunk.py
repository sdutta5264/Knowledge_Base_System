from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.database import Base
from pgvector.sqlalchemy import Vector

class DocumentChunk(Base):
    __tablename__ = "document_chunks_db"

    id = Column(Integer, primary_key = True, index= True)
    document_id = Column(Integer, ForeignKey("documents_knowledge_db.id", ondelete= "CASCADE"))
    chunk_text = Column(Text, nullable= False)
    chunk_index = Column(Integer, nullable= False)
    embedding= Column(Vector(384), nullable=True)