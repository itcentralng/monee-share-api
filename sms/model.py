from pydantic import BaseModel, Field


class SMSModel(BaseModel):
    date: str | None = None
    from_: str = Field(alias=("from"))
    id: str | None = None
    linkId: str | None = None
    text: str | None = None
    to: str
    networkCode: str | None = None

    class Config:
        populate_by_name = True

    def __init__(self, **data):
        if "Body" in data and data["Body"] is not None:
            data["text"] = data.pop("Body")

        if "From" in data and data["From"] is not None:
            data["from_"] = data.pop("From")
        super().__init__(**data)
