from pydantic import BaseModel, Field
from typing import Optional, List

class DocumentResponse(BaseModel):
    id: int
    filename: str
    extracted_characters: int
    total_chunks_created: int
    msg: str

class SearchQuery(BaseModel):
    question: str
    top_k: Optional[int] = 3

class SearchResultItem(BaseModel):
    chunk_text: str
    document_filename: str = Field(validation_alias= "filename")
    similarity_score: float

    model_config= {
        "form_attributes": True
    }

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    chat_history: List[ChatMessage]
    top_k: int= 3

class ChatResponse(BaseModel):
    answer: str
    source_documents: List[str]
    updated_chat_history: List[ChatMessage]