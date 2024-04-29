from pydantic import BaseModel


class Message(BaseModel):
    content: str
    response: str
    role: str
    user: str
