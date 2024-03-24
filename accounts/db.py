from tenacity import retry, stop_after_attempt, wait_exponential
from lib.db import convex_client


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def create_account(user):
    return convex_client.mutation("users:insert", user)


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def get_account(phone):
    return convex_client.mutation("users:getSingleByPhone", {"phone": phone})


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def verify_pin(phone, pin):
    return convex_client.mutation("users:verifyPin", {"phone": phone, "pin": pin})


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def add_transaction(payload):
    return convex_client.mutation("transactions:insert", payload)
