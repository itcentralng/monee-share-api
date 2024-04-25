from typing import Union
from pydantic import BaseModel, Field


class Command(BaseModel):
    command: str = Field(
        description="User's command, which can be one of: 'balance', 'create', 'transfer', 'buy utility', or 'help'. Typos like 'hlp' for 'help' should be corrected."
    )
    beneficiary: Union[str, None] = Field(
        description="Recipient of the funds. For 'create' command, provide the National ID Number (NIN) used for account creation."
    )
    amount: Union[str, int, float, None] = Field(
        description="Amount for the transaction. If written in words, convert to numbers. This field accepts numerical values representing the currency involved."
    )
    is_transaction: bool = Field(
        description="Indicates whether this is a transaction. If True, it signifies a financial transaction."
    )
    transaction_type: Union[str, None] = Field(
        description="Type of transaction, if applicable. Must be one of: 'transfer', 'utility'. Otherwise, None."
    )
