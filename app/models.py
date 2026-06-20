# app/models.py

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True)
    company = Column(String(100))
    role = Column(String(100))
    content = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
