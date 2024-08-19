from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    Float,
)

from database import Base


class User(Base):
    __tablename__ = "users"

    id_ = Column(Integer, primary_key=True)
    balance = Column(Float, default=0.0)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
