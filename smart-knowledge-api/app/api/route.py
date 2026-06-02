from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schema.note import NoteResponse, NoteCreate, NoteUpdate
from app.services.note_service import create_note, get_notes, remove_note, update_note_data
from typing import List
from app.db.dependencies import get_db
from app.schema.user import UserCreate, LoginRequest
from app.services.user_service import create_user, get_users, login_user
from app.core.auth import get_current_user
from app.models.user import User
from app.services.document_service import DocumentService
from app.schema.document import SearchQuery, SearchResultItem, ChatResponse, ChatRequest

router = APIRouter()

@router.get("/dummy")
def dummy_route():
    return {"message": "Dummy Route"}

@router.post("/notes", response_model=NoteResponse)
def add_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    return create_note(db, note, current_user)

@router.get("/notes", response_model=List[NoteResponse])
def list_notes(db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    return get_notes(db, current_user)

@router.put("/notes/{id}", response_model=NoteResponse)
def update_note(id: int, note_data: NoteUpdate, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    return update_note_data(id, note_data, db, current_user)

@router.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    return remove_note(id, db, current_user)

@router.post("/signup")
def signup(user: UserCreate, db = Depends(get_db)):
    return create_user(db, user)

@router.get("/get_users")
def listUsers(db = Depends(get_db)):
    return get_users(db)

@router.post("/login")
def login( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(db, form_data.username, form_data.password)

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {"message": "DB Connected Successfully"}
    except OperationalError as e:
        return HTTPException(status_code = 500, detail= "DB connection failed: "+ str(e))

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await DocumentService.process_and_save_document(db, file, current_user)

'''file: UploadFile = File(...) here UploadFile specifies the user needs to upload a file, 
File specifies the upload file will come from Form,
... specifies its mandatory'''

@router.post("/documents/search", response_model=List[SearchResultItem])
def search_documents(query: SearchQuery, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return DocumentService.search_similar_chunks(db, query.question, current_user, top_k = query.top_k)

@router.post("/documents/chat", response_model= ChatResponse)
def chat_with_documents(request: ChatRequest, db: Session= Depends(get_db), current_user= Depends(get_current_user)):
    response_data = DocumentService.process_chat_query(db, request, current_user.id)
    return ChatResponse.model_validate(response_data)
