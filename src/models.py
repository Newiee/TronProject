from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.now)