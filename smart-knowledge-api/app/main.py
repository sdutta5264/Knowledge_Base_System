from fastapi import FastAPI
from app.api.route import router
from app.db.database import Base, engine

from app.models.user import User
from app.models.note import Note
from app.models.document import Document

Base.metadata.create_all(engine)

app = FastAPI(title= "Smart Knowledge Api")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is running"}