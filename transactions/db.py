from tenacity import retry, stop_after_attempt, wait_exponential
from utils.db import convex_client


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def add_transaction(payload):
    return convex_client.query("transactions:insert", payload)
