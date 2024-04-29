from pydantic import BaseModel
from accounts.models import DBAccount


class UtilParam(BaseModel):
    user: DBAccount
    user_query_list: list
