from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]