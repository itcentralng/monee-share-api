import jwt
import time

payload = {
    "iss": "moneeshare.com",
    "sub": "1c535816a213693412a3f1162f6a021c",
    "aud": "https://api.sandbox.safehavenmfb.com",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600,  # Token valid for 1 hour
}

# Load your private key for signing the token
with open("keys/privatekey.pem", "r") as file:
    private_key = file.read()


def generate_accertion():
    # Generate the JWT token
    token = jwt.encode(payload, private_key, algorithm="RS256")
    print(token)
    return token
