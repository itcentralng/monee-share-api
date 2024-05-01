from pydantic import BaseModel, Field


class SMSModel(BaseModel):
    date: str = None
    from_: str = Field(alias=("from"))
    id: str = None
    linkId: str = None
    text: str = Field()
    to: str = None
    networkCode: str = None
