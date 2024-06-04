from accounts.models import CreateAccountParam, DBAccount
from lib import _signalwire as signalwire
from accounts import controller as account_controller
from messages import controller as message_controller
from templates.response_templates import PinResponses, Responses, UtilResponses
from transactions import controller as transaction_controller
from sms import controller as sms_controller
from utility import controller as util_controller


async def help(user_phone: str, command_str: str, willSendSMS: bool):
    if willSendSMS:
        await sms_controller.send_sms(Responses.HELP_SHORT, [user_phone])

    user_message = {
        "content": command_str,
        "role": "user",
        "phone": user_phone,
    }
    bot_message = {
        "content": Responses.HELP_SHORT,
        "role": "bot",
        "phone": user_phone,
    }
    await message_controller.add_messages(user_message, bot_message)
    return {"message": Responses.HELP}


async def balance(user_phone: str, command_str: str, willSendSMS: bool):
    user_db_account = await account_controller.get_account_from_db(user_phone)

    user_message = {
        "content": command_str,
        "role": "user",
        "phone": user_db_account.phone,
    }
    bot_message = {
        "content": PinResponses.PIN_CONFIRMATION,
        "role": "bot",
        "phone": user_db_account.phone,
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

    if willSendSMS:
        await sms_controller.send_sms(PinResponses.PIN_CONFIRMATION, [user_phone])

    await signalwire.make_call(user_db_account.phone)
    return {"message": PinResponses.PIN_CONFIRMATION}


async def util(user_phone: str, user_query_list: str, willSendSMS: bool):
    command_str = " ".join(user_query_list)
    user_db_account = await account_controller.get_account_from_db(user_phone)

    verified_meter = await util_controller.verify_meter(
        {
            "user": user_db_account,
            "user_query_list": user_query_list,
        }
    )

    if verified_meter:
        if willSendSMS:
            # TEMP
            await sms_controller.send_sms(
                UtilResponses.UTIL_CONFIRM.format(
                    amount=user_query_list[1],
                    meter_number=verified_meter.meter_no,
                    meter_owner=verified_meter.name,
                ),
                [user_phone],
            )

        # TEMP
        user_message = {
            "content": command_str,
            "role": "user",
            "phone": user_db_account.phone,
        }
        bot_message = {
            "content": UtilResponses.UTIL_CONFIRM.format(
                amount=user_query_list[1],
                meter_number=verified_meter.meter_no,
                meter_owner=verified_meter.name,
            ),
            "role": "bot",
            "phone": user_db_account.phone,
        }
        await message_controller.add_messages(user_message, bot_message)

        await transaction_controller.add_transaction(
            {
                "command": command_str,
                "status": "pending",
                "type": "util",
                "user": user_phone,
            }
        )

        await signalwire.make_call(user_db_account.phone)
        return UtilResponses.UTIL_CONFIRM.format(
            amount=user_query_list[1],
            meter_number=verified_meter.meter_no,
            meter_owner=verified_meter.name,
        )
    else:
        if willSendSMS:
            await sms_controller.send_sms(
                UtilResponses.UTIL_VERIFICATION_FAILED.format(
                    meter_number=user_query_list[2]
                ),
                [user_phone],
            )

        # TEMP
        user_message = {
            "content": command_str,
            "role": "user",
            "phone": user_db_account.phone,
        }
        bot_message = {
            "content": UtilResponses.UTIL_VERIFICATION_FAILED.format(
                meter_number=user_query_list[2]
            ),
            "role": "bot",
            "phone": user_db_account.phone,
        }
        await message_controller.add_messages(user_message, bot_message)

        return {
            "message": UtilResponses.UTIL_VERIFICATION_FAILED.format(
                meter_number=user_query_list[2]
            )
        }


async def create(user_phone: str, user_query_list: str, willSendSMS: bool):
    response = await account_controller.create(user_phone, user_query_list[1])
    if willSendSMS:
        await sms_controller.send_sms(response, [user_phone])
    return {"message": response}


async def transfer_funds(user_phone: str, user_query_list: str, willSendSMS: bool):
    response = await account_controller.transfer_funds(
        user_query_list[1], user_phone, user_query_list[2]
    )
    if response[0]:
        await transaction_controller.add_transaction(
            {
                "command": " ".join(user_query_list),
                "status": "pending",
                "type": "transfer",
                "user": user_phone,
            }
        )

        if willSendSMS:
            await sms_controller.send_sms(PinResponses.PIN_CONFIRMATION, [user_phone])
        await signalwire.make_call(user_phone)

    else:
        if willSendSMS:
            await sms_controller.send_sms(response, [user_phone])
    return response
