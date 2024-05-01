from accounts.models import DBAccount, SafeHavenAccount, CreateAccountParam
from templates.response_templates import AccountResponses
from . import db as database
from . import bank as haven
from accounts import controller as account_controller
from messages import controller as message_controller


async def get_account_from_db(phone: str):
    account = await database.get_account(phone)
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


# async def create(data: CreateAccountParam):
#     print(data.user)


# async def create(data):
#     sender, command = data.values()

#     payload = {
#         "firstName": f"customer_{sender.replace('+','')}",
#         "phoneNumber": sender,
#         "emailAddress": f"customer_{sender.replace('+','')}@moneeshare.com",
#         "externalReference": f"{sender.replace('+','')}",
#     }
#     account = await haven.create_account(payload)
#     print(account)

#     if not account.get("data"):
#         response = f"There was a problem creating account. Please try again later"
#         return response
#     else:
#         account = account.get("data")
#         payload = {
#             "safehavenId": account.get("_id"),
#             "firstName": account.get("subAccountDetails")["firstName"],
#             "lastName": account.get("subAccountDetails")["lastName"],
#             "phone": account.get("subAccountDetails")["phoneNumber"],
#             "email": account.get("subAccountDetails")["emailAddress"],
#             "account": account.get("accountNumber"),
#             "bvn": "",
#             "nin": command[1],
#             "password": "password",
#             "pin": "1234",
#         }

#         db_response = await database.create_account(payload)
#         print(db_response)

#     return account
