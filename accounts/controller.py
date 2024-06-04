from accounts.models import DBAccount, SafeHavenAccount, CreateAccountParam
from templates.response_templates import AccountResponses, TransferResponses
from . import db as database
from . import bank as haven
from accounts import controller as account_controller
from messages import controller as message_controller


async def get_account_from_db(phone: str):
    account = await database.get_account(phone)
    if "error" in account:
        return account
    return DBAccount(**account)


async def get_account_from_haven(account_id: str):
    account = await haven.get_account(account_id)
    if "error" in account:
        return account
    return SafeHavenAccount(**account)


async def has_funds(account_id: str, amount: float):
    return await haven.has_funds(account_id, amount)


async def get_balance(account_id: str):
    safehaven_account = await get_account_from_haven(account_id)
    if safehaven_account.accountNumber:
        return {"balance": safehaven_account.accountBalance}
    else:
        return {"error": "Could not get your account balance. Please try again"}


async def perform_get_balance(phone: str):
    sender_db_account = await account_controller.get_account_from_db(phone)
    balance_response = await get_balance(sender_db_account.safehavenId)
    if "error" in balance_response:
        bot_message = {
            "content": balance_response["error"],
            "role": "bot",
            "phone": sender_db_account.phone,
        }
        await message_controller.add_message(bot_message)

        return balance_response["error"]

    bot_message = {
        "content": AccountResponses.BALANCE.format(balance=balance_response["balance"]),
        "role": "bot",
        "phone": sender_db_account.phone,
    }
    await message_controller.add_message(bot_message)

    return AccountResponses.BALANCE.format(balance=balance_response["balance"])


async def verify_pin(data):
    (phone, pin) = data.values()
    return await database.verify_pin(phone, pin)


async def create(user_phone: str, nin: str):
    response = "Sorry this command is currently unavailable"
    bot_message = {
        "content": response,
        "role": "bot",
        "phone": user_phone,
    }
    await message_controller.add_message(bot_message)
    return response


async def transfer_funds(amount: str, user_phone: str, beneficiary: str):
    user_db_account = await get_account_from_db(user_phone)
    if "error" in user_db_account:
        response = [False, "It seems you don't have an account"]
    else:
        user_bank_account = await get_account_from_haven(user_db_account.safehavenId)
        if "error" in user_bank_account:
            response = [False, "Something went wrong, Try again"]
        else:
            beneficiary_db_account = await get_account_from_db(beneficiary)

            if "error" in beneficiary_db_account:
                response = [
                    False,
                    "Beneficiary does not have an account. Account creation is temporarily unavailable",
                ]
            else:
                if user_bank_account.accountBalance <= int(amount):
                    response = [False, TransferResponses.INSUFFICIENT_FUNDS]
                else:
                    response = [
                        True,
                        TransferResponses.SEND_CONFIRMATION.format(
                            amount=amount, beneficiary=beneficiary
                        ),
                    ]

    bot_message = {
        "content": response[1],
        "role": "bot",
        "phone": user_phone,
    }
    await message_controller.add_message(bot_message)
    return response
