from lib._africastalking import AfricasTalking

sms = AfricasTalking().send


async def send_sms(
    message: str,
    reciepients: list[str],
):
    sms(message, reciepients)
