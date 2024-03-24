from . import db as database
from . import bank as haven


async def create(data):
    sender, command = data.values()

    payload = {
        "firstName": f"customer_{sender.replace('+','')}",
        "phoneNumber": sender,
        "emailAddress": f"customer_{sender.replace('+','')}@moneeshare.com",
        "externalReference": f"{sender.replace('+','')}",
    }
    account = await haven.create_account(payload)
    print(account)

    if not account.get("data"):
        response = f"There was a problem creating account. Please try again later"
    else:
        account = account.get("data")
        payload = {
            "safehavenId": account.get("_id"),
            "firstName": account.get("subAccountDetails")["firstName"],
            "lastName": account.get("subAccountDetails")["lastName"],
            "phone": account.get("subAccountDetails")["phoneNumber"],
            "email": account.get("subAccountDetails")["emailAddress"],
            "account": account.get("accountNumber"),
            "bvn": "",
            "nin": command[1],
            "password": "password",
            "pin": "1234",
        }

        db_response = await database.create_account(payload)
        print(db_response)

        response = f"""Welcome to Monee Share
            Your account was created successfully.
            Use your phone number to send/receive money on Monee Share

            to fund your account from other banks use:
            Account Number: {account["accountNumber"]}
            Bank: Safehaven MFB

            For more infotmation, send  help"
        """

    return response


async def get_balance(data):
    (sender_account,) = data.values()
    safehaven_account = await haven.get_account(sender_account["safehavenId"])

    print(safehaven_account)
    if "data" in safehaven_account:
        response = f'Your balance is N{safehaven_account["data"]["accountBalance"]}'
    else:
        response = f"Could not get your account balance. Please try again"
    return response


async def get_account_from_db(data):
    (phone,) = data.values()
    return await database.get_account(phone)


async def get_account_from_haven(data):
    (account_id,) = data.values()
    return await haven.get_account(account_id)


async def has_funds(data):
    (account_id, amount) = data.values()
    return await haven.has_funds(account_id, amount)


async def verify_pin(data):
    (phone, pin) = data.values()
    return await database.verify_pin(phone, pin)
