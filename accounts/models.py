from pydantic import BaseModel, Field


class DBAccount(BaseModel):
    id: str = Field(alias="_id")
    safehavenId: str
    firstName: str
    lastName: str
    phone: str
    email: str
    account: str
    pin: str
    nin: str
    bvn: str
    password: str
    _creationTime: float


class SubAccount(BaseModel):
    _id: str
    firstName: str
    lastName: str
    phoneNumber: str
    emailAddress: str


class SafeHavenAccount(BaseModel):
    accountNumber: float
    accountName: str
    accountType: str
    bvn: str
    accountBalance: float
    subAccount: SubAccount = Field(alias="subAccountDetails")


class CreateAccountParam(BaseModel):
    user: DBAccount
    user_query_list: list
