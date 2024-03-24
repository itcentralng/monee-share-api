from tenacity import retry, stop_after_attempt, wait_exponential
from lib.db import convex_client


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def add_message(payload):
    return convex_client.mutation("messages:send", payload)
