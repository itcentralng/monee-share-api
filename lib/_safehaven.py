import os
from dotenv import load_dotenv
import requests
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from lib._crypt0 import generate_accertion


load_dotenv()


class SafeHaven:
    TOKEN = None
    RTOKEN = None
    ACCERTION = generate_accertion()
    # ACCERTION = os.environ.get("SAFEHAVEN_ACCERTION")
    CLIENT_ID = os.environ.get("SAFEHAVEN_CLIENT_ID")
    EXPIRES_IN = None
    LAST_TOKEN_REFRESH = None
    BASE_URL = "https://api.sandbox.safehavenmfb.com"

    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60)
    )
    async def post(self, url, payload, has_token=False):
        if not self.TOKEN:
            await self.get_token()

        headers = {"accept": "application/json", "content-type": "application/json"}
        if has_token:
            headers["authorization"] = f"Bearer {self.TOKEN}"
            headers["ClientID"] = f"1c535816a213693412a3f1162f6a021c"

        response = requests.post(self.BASE_URL + url, json=payload, headers=headers)

        if (
            "error_description" in response.json()
            and "invalid client_assertion"
            in response.json()["error_description"].lower()
        ):
            self.ACCERTION = generate_accertion()
            await self.get_token()
            response = requests.post(self.BASE_URL + url, json=payload, headers=headers)
        if (
            "message" in response.json()
            and "expired token" in response.json()["message"].lower()
            and self.RTOKEN
        ):
            print("refresh")
            await self.refresh_token()
            response = requests.post(self.BASE_URL + url, json=payload, headers=headers)

        print("POST")
        return response.json()

    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60)
    )
    async def get(self, url):
        if not self.TOKEN:
            await self.get_token()

        headers = {
            "accept": "application/json",
            "ClientID": "1c535816a213693412a3f1162f6a021c",
            "authorization": f"Bearer {self.TOKEN}",
        }

        response = requests.get(self.BASE_URL + url, headers=headers)

        if (
            "error_description" in response.json()
            and "invalid client_assertion"
            in response.json()["error_description"].lower()
        ):
            self.ACCERTION = generate_accertion()
            await self.get_token()
            response = requests.get(self.BASE_URL + url, headers=headers)
        elif (
            "message" in response.json()
            and "expired token" in response.json()["message"].lower()
            and self.RTOKEN
        ):
            print("refresh")
            await self.refresh_token()
            response = requests.post(self.BASE_URL + url, headers=headers)

        print("GET")
        return response.json()

    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60)
    )
    async def get_token(self):

        if not self.ACCERTION:
            return {"error": "No accertion token found"}

        url = "/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": self.ACCERTION,
            "client_id": self.CLIENT_ID,
        }
        headers = {"accept": "application/json", "content-type": "application/json"}

        try:
            response = requests.post(
                self.BASE_URL + url, json=payload, headers=headers
            ).json()
            print(response)
            self.TOKEN = response["access_token"]
            self.RTOKEN = response["refresh_token"]
            self.EXPIRES_IN = response["expires_in"]
            self.LAST_TOKEN_REFRESH = time.time()

        except Exception as error:
            print(error)
            return {"error": "Could not get access token"}

    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60)
    )
    async def refresh_token(self):

        if not self.RTOKEN:
            return {"error": "No refresh token found"}

        url = "/oauth2/token"
        payload = {
            "grant_type": "refresh_token",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_id": self.CLIENT_ID,
            "client_assertion": self.ACCERTION,
            "refresh_token": self.RTOKEN,
        }
        headers = {"accept": "application/json", "content-type": "application/json"}

        try:
            response = requests.post(
                self.BASE_URL + url, json=payload, headers=headers
            ).json()
            print(response)
            self.TOKEN = response["access_token"]
            self.RTOKEN = response["refresh_token"]
            self.EXPIRES_IN = response["expires_in"]
            self.LAST_TOKEN_REFRESH = time.time()

        except Exception as error:
            print(error)
            return {"error": "Could not get access token"}


safehaven_client = SafeHaven()
