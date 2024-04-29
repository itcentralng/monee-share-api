import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv()

payload = {
    "iss": "moneeshare.com",
    "sub": "1c535816a213693412a3f1162f6a021c",
    "aud": "https://api.sandbox.safehavenmfb.com",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600,  # Token valid for 1 hour
}

# Load your private key for signing the token
IS_PRODUCTION = os.environ.get("PRODUCTION_ENV")

if IS_PRODUCTION == "True":
    print("Production Env")
    file_path = "/etc/secrets/privatekey.pem"
else:
    print("Dev Env")
    file_path = "etc/secrets/privatekey.pem"


with open(file_path, "r") as file:
    private_key = file.read()


def generate_accertion():
    # Generate the JWT token
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
