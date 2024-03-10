import os
from dotenv import load_dotenv
import africastalking
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

africastalking.initialize(
    username=os.environ.get("AFRICASTALKING_USERNAME"),
    api_key=os.environ.get("AFRICASTALKING_API_KEY"),
)


class AfricasTalking:
    sms = africastalking.SMS

    @retry(
    stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    def send(self, message, recipients,sender):
        try:
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")
