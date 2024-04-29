from fastapi import APIRouter, Request
from pydantic import BaseModel
from lib.db import DB
from lib._safehaven import SafeHaven
from accounts import (
    controller as account_controller,
    db as account_DB,
    bank as account_haven,
)
from utility import controller
from transactions import controller


router = APIRouter()
database = DB()
haven = SafeHaven()


class User(BaseModel):
    phone: str
    firstName: str
    lastName: str
    password: str
    pin: str
    email: str
    nin: str
    bvn: str


@router.post("/user")
async def create_user(user: Request):
    print(await user.json())
    user = await user.json()
    user_from_db = await account_controller.get_account_from_db(
        {"phone": user["phone"]}
    )
    print(user_from_db)
    if user_from_db.get("_id"):
        return {"error": "User already exists"}
    else:
        payload = {
            "firstName": f"customer_{user['firstName']}",
            "phoneNumber": user["phone"],
            "emailAddress": f"customer_{user['phone'].replace("+","")}@moneeshare.com",
            "externalReference": user['phone'].replace("+",""),
        }
        account = await account_haven.create_account(payload)

        account = account.get("data")
        print(account)
        # payload = {
        #     "safehavenId": account.get("subAccountDetails")["_id"],
        #     "firstName": account.get("subAccountDetails")["firstName"],
        #     "lastName": account.get("subAccountDetails")["lastName"],
        #     "phone": account.get("subAccountDetails")["phoneNumber"],
        #     "email": account.get("subAccountDetails")["emailAddress"],
        #     "account": account.get("accountNumber"),
        #     "bvn": "",
        #     "nin": user.get("nin", "1234567890"),
        #     "password": user.get("password", ""),
        # }
        # db_account = await account_DB.create_account()
        
        # response = await database.add_message(
        #     {
        #         "phone": user["phone"],
        #         "role": "bot",
        #         "content": response,
        #     }
        # )
    return {"message": "Sign up successfull"}


@router.post("/sms")
async def receive_sms(request: Request):

    req = await request.json()
    msg = req.get("content").lower()
    sender = req.get("phone")

    command = msg.split()

    response = ""
    sender_account = await account_controller.get_account_from_db({"phone": sender})
    print(command, sender)
    print(sender_account)

    # HELP
    if "help" in msg:
        response = f"""List of commands:\n1. create -> create [NIN/BVN]\n2. send -> send [AMOUNT] [PHONE_NUMBER]\n3. util -> util [AMOUNT] [METER_NUM] [STATE]\n4. balance -> balance\n5. help -> help"""
    # END OF HELP

    elif not len(sender_account) and "create" not in msg:
        response = f"""It seems you don't have an account. Send create NIN/BVN" to create your account."""

    elif len(sender_account) and "create" in msg:
        response = f"""It seems you already have an account.\nSend "help" for more information."""

    # BALANCE
    elif "balance" in msg:
        response = await account_controller.get_balance(
            {"sender_account": sender_account}
        )
    # END OF BALANCE

    elif len(command) < 3:
        response = f'Not enough information provided. please send "help" for details on the command'

    # START OF CREATE
    elif "create" in msg:
        response = await account_controller.create(
            {"sender": sender, "command": command}
        )

    # END OF CREATE

    # UTIL
    elif "util" in msg:
        response = await controller.buy(
            {"sender_account": sender_account, "command": command}
        )
    # END OF UTIL

    # TRANSFER
    elif "send" in msg:
        response = await controller.send(
            {
                "sender": sender,
                "sender_account": sender_account,
                "command": command,
                "msg": msg,
            }
        )

    # END OF SEND MONEY

    else:
        response = f'Command not understood.\nText "help" for the list of all commands'
    # END OF TRANSFER

    response = await database.add_message(
        {
            "phone": sender,
            "role": "bot",
            "content": response,
        }
    )
    print(response)
