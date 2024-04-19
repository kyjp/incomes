from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True)
    ptice = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())