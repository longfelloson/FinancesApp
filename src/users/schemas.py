from typing import Union

from pydantic import BaseModel, EmailStr


class UserCredentials(BaseModel):
    email: EmailStr
    hashed_password: bytes


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UpdateBalance(BaseModel):
    amount: Union[int, float]
