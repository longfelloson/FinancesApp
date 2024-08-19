from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field

from operations.enums import OperationType


class Operation(BaseModel):
    id_: int
    name: str
    amount: float
    type_: OperationType
    created_at: datetime

    class Config:
        from_attributes = True


class CreateOperation(BaseModel):
    name: str
    amount: Union[int, float]
    type_: OperationType = Field(default=None)
