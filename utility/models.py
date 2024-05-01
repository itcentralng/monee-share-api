from pydantic import BaseModel, Field
from accounts.models import DBAccount


class UtilParam(BaseModel):
    user: DBAccount
    user_query_list: list


class UtilModel(BaseModel):
    name: str
    address: str
    meter_no: str = Field(alias="meterNo")
    categoryId: str
    vendType: str
    disco: str


class DiscoModel(BaseModel):
    name: str
    states: list[str]
