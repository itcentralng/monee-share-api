from pydantic import BaseModel, Field


class TransactionModel(BaseModel):
    _creationTime: float
    id: str = Field(alias="_id")
    command: str
    status: str
    type: str
    user: str


class TransactionInputModel(BaseModel):
    command: str
    status: str
    type: str
    user: str
