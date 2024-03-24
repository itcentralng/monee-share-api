import os
from dotenv import load_dotenv
from convex import ConvexClient
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()
CONVEX_URL = os.environ.get("CONVEX_URL")
convex_client = ConvexClient(os.environ.get("CONVEX_URL"))
