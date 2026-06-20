from pydantic import BaseModel

class GenerateRequest(BaseModel):
    company: str
    role: str
    job_description: str
