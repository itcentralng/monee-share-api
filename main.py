import os
from dotenv import load_dotenv
from convex import ConvexClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from utils.api import transform_request
from utils.africastalking import AfricasTalking

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

CONVEX_URL = os.environ.get("CONVEX_URL")

client = ConvexClient(os.environ.get("CONVEX_URL"))

@app.get("/")
async def home():
    return {"app": "Money share", "status": "ok"}


@app.post("/sms")
async def receive_sms(request: Request):
    request = await transform_request(request)
    msg = request["text"]
    to = request["to"]
    sender = request["from"]
    # date = request["date"]

    commands = msg.split()

    response = ""
    if "create" in msg:
        response = f"Created account successfully"
    elif "balance" in msg:
        response = f"Your balance is xxxxxx"
    elif "send" in msg:
        response = f"Sent xxxxx to +234xxx successfully"
    elif "util" in msg:
        response = f"Your token: xxxxxxxxxxxx"
    else:
        response = f'Command not understood.\nTry texting "help" to 9011 for the list of all commands'

    AfricasTalking.send(AfricasTalking,response, [sender], to)