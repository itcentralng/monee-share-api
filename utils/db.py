import os
from dotenv import load_dotenv
from convex import ConvexClient
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
CONVEX_URL = os.environ.get("CONVEX_URL")
convex_client = ConvexClient(os.environ.get("CONVEX_URL"))


class DB:
    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60)
    )
    async def add_message(self, payload):
        return convex_client.mutation("messages:send", payload)
