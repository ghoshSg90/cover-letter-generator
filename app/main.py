# app/main.py
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import CoverLetter
from app.services.llm_service import generate_cover_letter
from app.services.pdf_service import create_pdf
from app.requestModel import GenerateRequest

app = FastAPI()

class CoverLetterRequest(BaseModel):
    company: str
    role: str
    content_path: str

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
        content_path=request.content_path
    )

    session.add(coverletter)
    session.commit()

    session.refresh(coverletter)

    session.close()

    return {
        "id": coverletter.id,
        "message": "Created"
    }


@app.post("/generate")
def generate(request: GenerateRequest):

    session = SessionLocal()

    try:

        cover_letter_text = generate_cover_letter(
            request.company,
            request.role,
            request.job_description
        )

        filename = f"{uuid.uuid4()}.pdf"

        pdf_path = (
            f"storage/coverletters/{filename}"
        )

        create_pdf(
            cover_letter_text,
            pdf_path
        )
        print(CoverLetter.__table__.columns.keys())
        coverletter = CoverLetter(
            company=request.company,
            role=request.role,
            content_path=pdf_path
        )

        session.add(coverletter)
        session.commit()
        session.refresh(coverletter)

        return {
            "id": coverletter.id,
            "pdf_path": pdf_path
        }

    finally:
        session.close()

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
    coverletter.content_path = request.content_path

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
