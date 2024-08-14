from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Operation(Base):
    __tablename__ = "operations"

    id_ = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    type_ = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
