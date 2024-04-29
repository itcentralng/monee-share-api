from lib._africastalking import AfricasTalking

sms = AfricasTalking().send


async def send_sms(
    message: str = "hello world",
    reciepients: list[str] = ["+2348181114416", "+2348026075864"],
):
    sms(message, reciepients)
