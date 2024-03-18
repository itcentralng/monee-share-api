from tenacity import retry, stop_after_attempt, wait_exponential
from utils.db import convex_client


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def get_discos(state):
    return convex_client.query("discos:get", {"state": state})


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
async def get_discos_by_state(state):
    return convex_client.query("serviceCategories:getByState", {"state": state})
