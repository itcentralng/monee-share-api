from tenacity import retry, stop_after_attempt, wait_exponential
from lib.db import convex_client
from messages.models import Message


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def add_message(message: Message):
    return convex_client.mutation("messages:send", message)


async def add_messages(user_message: Message, bot_message: Message):
    user_res = convex_client.mutation("messages:send", user_message)
    bot_res = convex_client.mutation("messages:send", bot_message)
    return [user_res, bot_res]
