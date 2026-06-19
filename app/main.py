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

@app.get("/coverletters/{id}")
def get_coverletter(id: int):

    session = SessionLocal()

    coverletter = (
        session.query(CoverLetter)
        .filter(CoverLetter.id == id)
        .first()
    )

    session.close()

    return coverletter


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

@app.put("/coverletters/{id}")
def update_coverletter(
    id: int,
    request: CoverLetterRequest
):
    session = SessionLocal()

    coverletter = (
        session.query(CoverLetter)
        .filter(CoverLetter.id == id)
        .first()
    )

    if not coverletter:
        session.close()
        return {"error": "Cover letter not found"}

    coverletter.company = request.company
    coverletter.role = request.role
    coverletter.content = request.content

    session.commit()
    session.refresh(coverletter)

    session.close()

    return {
        "message": "Updated successfully",
        "id": id
    }

@app.delete("/coverletters/{id}")
def delete_coverletter(id: int):

    session = SessionLocal()

    coverletter = (
        session.query(CoverLetter)
        .filter(CoverLetter.id == id)
        .first()
    )

    if not coverletter:
        session.close()
        return {"error": "Cover letter not found"}

    session.delete(coverletter)
    session.commit()

    session.close()

    return {
        "message": "Deleted successfully",
        "id": id
    }
