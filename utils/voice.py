from __future__ import print_function
import os
import africastalking
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()

class VOICE:
    def __init__(self):
		# Set your app credentials
        self.username=os.environ.get("AFRICASTALKING_USERNAME")
        self.api_key=os.environ.get("AFRICASTALKING_API_KEY")
        self.NUMBER=os.environ.get("AFRICASTALKING_VOICE_NUM")
        
		# Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
		# Get the voice service
        self.voice = africastalking.Voice

    @retry(
        stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=60))
    def call(self):
        # Set your Africa's Talking phone number in international format
        callFrom = self.NUMBER
        # Set the numbers you want to call to in a comma-separated list
        callTo   = ["+2348026075864"]
        try:
			# Make the call
            result = self.voice.call(callFrom, callTo)
            print (result)
        except Exception as e:
            print ("Encountered an error while making the call:%s" %str(e))

if __name__ == '__main__':
    VOICE().call()