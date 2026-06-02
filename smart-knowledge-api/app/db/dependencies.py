from app.db.database import SessionLocal

def get_db():               #This is a generator Function
    db = SessionLocal() #Generates the DB instances
    try:
        yield db        #Stop the execution here
    finally:
        db.close()