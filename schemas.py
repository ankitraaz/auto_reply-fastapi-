# schemas.py
from pydantic import BaseModel

class NoteCreate(BaseModel):  # Client se aane wala data
    title: str
    content: str

class NoteOut(NoteCreate):  # Client ko bhejne wala data
    id: int

    class Config:
        model_config = {
    "from_attributes": True
}
