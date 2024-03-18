from utils.db import DB
from utils.haven import SafeHaven

database = DB()
haven = SafeHaven()


async def create_account(data):
    sender, command = data.values()

    payload = {
        "firstName": f"customer_{sender.replace(" + "," ")}",
        "phoneNumber": sender,
        "emailAddress": f"customer_{sender.replace(" + "," ")}@moneeshare.com",
        "externalReference": f"{sender.replace(" + "," ")}",
    }
    account = await haven.create_account(payload)
    print(account)

    if not account.get("data", None):
        response = f"There was a problem creating account. Please try again later"
    else:
        account = account.get("data")
        payload = {
            "safehavenId": account.get("subAccountDetails")["_id"],
            "firstName": account.get("subAccountDetails")["firstName"],
            "lastName": account.get("subAccountDetails")["lastName"],
            "phone": account.get("subAccountDetails")["phoneNumber"],
            "email": account.get("subAccountDetails")["emailAddress"],
            "account": account.get("accountNumber"),
            "bvn": "",
            "nin": command[1],
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

    # payload = {
    #     "firstName": f"customer_{sender.replace(" + "," ")}",
    #     "phoneNumber": sender,
    #     "emailAddress": f"customer_{sender.replace(" + "," ")}@moneeshare.com",
    #     "externalReference": f"{sender.replace(" + "," ")}",
    # }
    # account = await haven.create_account(payload)
    # print(account)

    # if not account.get("data", None):
    #     response = f"There was a problem creating account. Please try again later"
    # else:
    #     account = account.get("data")
    #     payload = {
    #         "safehavenId": account.get("subAccountDetails")["_id"],
    #         "firstName": account.get("subAccountDetails")["firstName"],
    #         "lastName": account.get("subAccountDetails")["lastName"],
    #         "phone": account.get("subAccountDetails")["phoneNumber"],
    #         "email": account.get("subAccountDetails")["emailAddress"],
    #         "account": account.get("accountNumber"),
    #         "bvn": "",
    #         "nin": command[1],
    #     }

    #     db_response = await database.create_account(payload)
    #     print(db_response)

    #     response = f"""Welcome to Monee Share
    #         Your account was created successfully.
    #         Use your phone number to send/receive money on Monee Share

    #         to fund your account from other banks use:
    #         Account Number: {account["accountNumber"]}
    #         Bank: Safehaven MFB

    #         For more infotmation, send  help"
    #     """
