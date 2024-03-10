import os
from dotenv import load_dotenv
from convex import ConvexClient
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
CONVEX_URL = os.environ.get("CONVEX_URL")


class DB:
    convex_client = ConvexClient(os.environ.get("CONVEX_URL"))

    @retry(
    stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    async def get_discos(self, state):
        return self.convex_client.query("discos:get", {"state": state})

    @retry(
    stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    async def create_account(self, user):
        return self.convex_client.mutation("users:insert", user)

    @retry(
    stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    async def get_account(self, phone_number):
        return self.convex_client.query("users:getSingle", {"phone_number": phone_number})
    
    @retry(
    stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    async def get_discos_by_state(self, state):
        return self.convex_client.query("serviceCategories:getByState", {"state": state})
