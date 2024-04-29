from pydantic import BaseModel


class CallModel(BaseModel):
    From: str
    Digits: str
    To: str
