import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
import time


load_dotenv()
TOKEN = None
RTOKEN = None
ACCERTION = os.environ.get("SAFEHAVEN_ACCERTION")
CLIENT_ID = os.environ.get("SAFEHAVEN_CLIENT_ID")
EXPIRES_IN = None
LAST_TOKEN_REFRESH = None


class SafeHaven:
    def __init__(self):
        self.BASE_URL = "https://api.sandbox.safehavenmfb.com"

    async def post(self, url, payload, has_token=False):
        headers = {"accept": "application/json", "content-type": "application/json"}
        if has_token:
            headers["authorization"] = f"Bearer {TOKEN}"

        response = requests.post(self.BASE_URL + url, json=payload, headers=headers)
        print(response.text)  # REMOVE LATER
        return response.json()

    async def get(self, url):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {TOKEN}",
        }

        response = requests.get(self.BASE_URL + url, headers=headers)
        print(response.text)  # REMOVE LATER
        return response.json()

    async def get_token(self):
        global TOKEN, RTOKEN, LAST_TOKEN_REFRESH, EXPIRES_IN

        if not ACCERTION:
            raise HTTPException(status_code=500, detail="No accertion token found")

        url = "/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": ACCERTION,
            "client_id": CLIENT_ID,
        }
        try:
            response = await self.post(url, payload)
            if "access_token" in response:
                TOKEN = response["access_token"]
                RTOKEN = response["refresh_token"]
                EXPIRES_IN = response["expires_in"]
                LAST_TOKEN_REFRESH = time.time()

        except Exception as error:
            print(error)
            raise HTTPException(status_code=500, detail="Could not get access token")

    async def refresh_token(self):

        if not RTOKEN:
            raise HTTPException(status_code=500, detail="No refresh token found")

        url = "/oauth2/token"

        payload = {
            "grant_type": "refresh_token",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_id": CLIENT_ID,
            "client_assertion": ACCERTION,
            "refresh_token": RTOKEN,
        }

        try:
            response = await self.post(url, payload)
            if "access_token" in response:
                TOKEN = response["access_token"]
                RTOKEN = response["refresh_token"]
                EXPIRES_IN = response["expires_in"]
                LAST_TOKEN_REFRESH = time.time()
        except Exception as error:
            print(error)
            raise HTTPException(status_code=500, detail="Could not get access token")

        print(response)
