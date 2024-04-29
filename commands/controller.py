from lib import _signalwire as signalwire
from accounts import controller as account_controller
from messages import controller as message_controller
from templates.response_templates import PinResponses, Responses
from transactions import controller as transaction_controller
from sms import controller as sms_controller


async def help(user_phone: str, willSendSMS: bool):

    if willSendSMS:
        await sms_controller.send_sms(Responses.HELP, [user_phone])
    return {"message": Responses.HELP}


async def balance(user_phone: str, command_str: str, willSendSMS: bool):
    sender_db_account = await account_controller.get_account_from_db("+2348026075864")

    if willSendSMS:
        await sms_controller.send_sms(PinResponses.PIN_CONFIRMATION, [user_phone])

    user_message = {
        "content": command_str,
        "role": "user",
        "phone": sender_db_account.phone,
    }
    bot_message = {
        "content": PinResponses.PIN_CONFIRMATION,
        "role": "bot",
        "phone": sender_db_account.phone,
    }
    await message_controller.add_messages(user_message, bot_message)

    await transaction_controller.add_transaction(
        {
            "command": command_str,
            "status": "pending",
            "type": "balance",
            "user": user_phone,
        }
    )
    await signalwire.make_call(sender_db_account.phone)
    return {"message": PinResponses.PIN_CONFIRMATION}
