from tenacity import retry, stop_after_attempt, wait_exponential
from lib.db import convex_client
from transactions.models import TransactionInputModel, TransactionModel


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def add_transaction(transaction: TransactionInputModel):
    return convex_client.mutation("transactions:insert", transaction)


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def get_transaction(phone: str):
    transaction = convex_client.query("transactions:getSingleByPhone", {"phone": phone})
    print(transaction)
    if "error" not in transaction:
        return TransactionModel(**transaction)
    return None
