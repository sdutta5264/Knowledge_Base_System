from http.client import HTTPException

from app.schema.note import NoteCreate, NoteResponse, NoteUpdate
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.user import User

notes_db = []
note_id_counter = 1

# def create_note(note: NoteCreate) -> NoteResponse:
#     global note_id_counter
#
#     new_note = {
#         "id": note_id_counter,
#         "title": note.title,
#         "content": note.content
#     }
#
#     notes_db.append(new_note)
#     note_id_counter = note_id_counter + 1
#     print(notes_db)
#
#     return NoteResponse.model_validate(new_note)

def create_note(db: Session, note: NoteCreate, user: User) -> NoteResponse:
    print("user id::",user.id)
    db_note = Note(
        title = note.title,
        content = note.content,
        user_id = user.id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return NoteResponse.model_validate(db_note)

# def get_notes() -> List[NoteResponse]:
#     #return [NoteResponse(**note) for note in notes_db]
#     return [NoteResponse.model_validate(note) for note in notes_db]

def get_notes(db: Session, user: User) -> List[NoteResponse]:
    notes = db.query(Note).filter(Note.user_id == user.id).all()
    print(notes)
    return [NoteResponse.model_validate(note) for note in notes]

def remove_note(id: int, db: Session, user: User):

    print(f"id : {id}")

    note  = db.query(Note).filter(Note.id == id, Note.user_id == user.id).first()
    if not note:
        return {"error" : "Note not found"}
    db.delete(note)
    db.commit()

    return {"msg" : "Deleted Successfully"}

def update_note_data(id: int, note_data: NoteUpdate, db: Session, user: User):
    note = db.query(Note).filter(Note.id == id, Note.user_id == user.id).first()

    if not note:
        raise HTTPException(status_code = 404, detail = "Note not found.")

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)

    return NoteResponse.model_validate(note)
