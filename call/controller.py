from typing import Annotated
from fastapi import APIRouter, Depends, Form
from call.models import CallModel
from templates.response_templates import PinResponses, Responses
from transactions import controller as transaction_controller
from accounts import controller as account_controller
from messages import controller as message_controller
from sms import controller as sms_controller


router = APIRouter()


async def get_data(
    From: Annotated[str, Form()],
    Digits: Annotated[str, Form()],
    To: Annotated[str, Form()],
) -> CallModel:
    return CallModel(From=From, Digits=Digits, To=To)


@router.post("")
async def call_handler(call: Annotated[CallModel, Depends(get_data)]):
    print(call.Digits)
    user_phone = call.From
    if "+234" not in call.From:
        user_phone = call.To

    sender_db_account = await account_controller.get_account_from_db(user_phone)

    if sender_db_account.pin != call.Digits:
        await sms_controller.send_sms(PinResponses.PIN_INCORRECT, [user_phone])

        bot_message = {
            "content": PinResponses.PIN_INCORRECT,
            "role": "bot",
            "phone": sender_db_account.phone,
        }
        await message_controller.add_message(bot_message)
        return PinResponses.PIN_INCORRECT

    response = await transaction_controller.get_and_perform(user_phone)
    print(response)

    # return transaction
