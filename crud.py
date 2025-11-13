# crud.py
from sqlalchemy.orm import Session
from models import Note
from schemas import NoteCreate

def create_note(db: Session, note: NoteCreate):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_notes(db: Session):
    return db.query(Note).all()
