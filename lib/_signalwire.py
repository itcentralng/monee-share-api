from fastapi import FastAPI
from lib.db import convex_client as database
from lib._safehaven import safehaven_client as haven
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = FastAPI()


def make_call(to_number):
    # Load values from .env file or any other configuration mechanism you're using
    account_sid = os.getenv("SIGNALWIRE_PROJECT_ID")
    auth_token = os.getenv("SIGNALWIRE_AUTHTOKEN")
    from_number = os.getenv("SIGNALWIRE_FROM_NUMBER")
    laml_url = os.getenv("SIGNALWIRE_LAML_URL")

    # Construct the payload
    payload = {"Url": laml_url, "From": from_number, "To": to_number}

    # Make the request
    response = requests.post(
        f"https://monee-share.signalwire.com/api/laml/2010-04-01/Accounts/{account_sid}/Calls",
        auth=(account_sid, auth_token),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data=payload,
    )

    # Check if the request was successful
    if response.status_code == 201:
        print("Call successfully initiated.")
    else:
        print(f"Failed to initiate call. Status code: {response.status_code}")
