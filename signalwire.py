from fastapi import FastAPI, Request
from signalwire.rest import Client

app = FastAPI()

# Replace with your credentials
client = Client(project="YOUR_PROJECT_ID", token="YOUR_API_TOKEN")


@app.post("/receive-sms")
async def handle_incoming_sms(request: Request):
    """
    Handles incoming SMS messages from SignalWire.
    """
    data = await request.json()

    # Access message information from the request body
    from_number = data.get("From")
    to_number = data.get("To")
    message_body = data.get("Body")

    # Process the received message (e.g., store it, send a response)
    # This is where you would add your application logic
    print(
        f"Received SMS: From: {from_number}, To: {to_number}, Message: {message_body}"
    )

    # You can optionally send a response using LaML
    # message_response = MessageResponse()
    # message_response.say("Thanks for your message!")
    # return message_response

    return {"message": "SMS Received!"}
