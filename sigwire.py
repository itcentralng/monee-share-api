# from fastapi import FastAPI, Request
# from signalwire.rest import Client

# app = FastAPI()

# # Replace with your credentials
# client = Client(project="YOUR_PROJECT_ID", token="YOUR_API_TOKEN")


# @app.post("/receive-sms")
# async def handle_incoming_sms(request: Request):
#     """
#     Handles incoming SMS messages from SignalWire.
#     """
#     data = await request.json()

#     # Access message information from the request body
#     from_number = data.get("From")
#     to_number = data.get("To")
#     message_body = data.get("Body")

#     # Process the received message (e.g., store it, send a response)
#     # This is where you would add your application logic
#     print(
#         f"Received SMS: From: {from_number}, To: {to_number}, Message: {message_body}"
#     )

#     # You can optionally send a response using LaML
#     # message_response = MessageResponse()
#     # message_response.say("Thanks for your message!")
#     # return message_response

#     return {"message": "SMS Received!"}

from signalwire.relay.consumer import Consumer
from dotenv import load_dotenv
import os
from signalwire.rest import Client as signalwire_client

load_dotenv()
client = signalwire_client(
    os.environ.get("SIGNALWIRE_PROJECT_ID"), os.environ.get("SIGNALWIRE_AUTHTOKEN")
)


class CustomConsumer(Consumer):
    def setup(self):
        self.project = os.environ.get("SIGNALWIRE_PROJECT_ID")
        self.token = os.environ.get("SIGNALWIRE_AUTHTOKEN")
        self.number = os.environ.get("SIGNALWIRE_FROM_NUMBER")
        self.contexts = ["home", "office"]

    async def ready(self):
        # Consumer is successfully connected with Relay.
        # You can make calls or send messages here..

        msg_response = await self.client.messaging.send(
            from_number=self.number,
            to_number="+2348181114416",
            context="office",
            body="Hello from signalwire",
        )
        print(msg_response.successful)

    async def on_incoming_call(self, call):
        result = await call.answer()
        if result.successful:
            print("Call answered..")

    async def on_incoming_message(self, message):
        message_body = message.body
        sender_number = message.from_number
        msg_response = await self.client.messaging.send(
            from_number=self.number,
            to_number=sender_number,
            context="office",
            body="Hello from signalwire",
        )
        print(msg_response.successful)
        print(f"Received message from: {sender_number} {message_body}")
        return super().on_incoming_message(message)


# Run your consumer..
consumer = CustomConsumer()
consumer.run()
