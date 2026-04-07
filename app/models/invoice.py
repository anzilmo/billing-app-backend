from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)