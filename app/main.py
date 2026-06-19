# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import CoverLetter

app = FastAPI()

class CoverLetterRequest(BaseModel):
    company: str
    role: str
    content: str

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/coverletters")
def get_coverletters():
    session = SessionLocal()

    data = session.query(CoverLetter).all()

    session.close()

    return data

@app.post("/coverletters")
def create_coverletter(request: CoverLetterRequest):

    session = SessionLocal()

    coverletter = CoverLetter(
        company=request.company,
        role=request.role,
        content=request.content
    )

    session.add(coverletter)
    session.commit()

    session.refresh(coverletter)

    session.close()

    return {
        "id": coverletter.id,
        "message": "Created"
    }
