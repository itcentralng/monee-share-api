from lib._safehaven import safehaven_client


async def get_accounts():

    url = "/accounts?limit=100&isSubAccount=true"

    try:
        response = await safehaven_client.get(url)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not get accounts"}


async def get_account(account_id):

    url = f"/accounts/{account_id}"

    try:
        response = await safehaven_client.get(url)
        return response["data"]

    except Exception as error:
        print(error)
        return {"error": "Could not get account"}


async def create_account(payload):

    url = "/accounts/subaccount"

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not create account"}


async def has_funds(account_id, amount):
    account = await get_account(account_id)
    print(account)
    if "data" in account:
        return [
            int(account["data"]["accountBalance"]) > int(amount),
            account["data"]["accountBalance"],
        ]

    elif account.get("statusCode") == 403:
        return [False, None]


async def initiate_verify_nin(payload):
    url = "/identity/v2"

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        if response["statusCode"] != 200:
            return [False, response.get("data")["_id"]]
        return [True, response.get("data")["_id"]]

    except Exception as error:
        print(error)
        return {"error": "Could not create account"}


async def confirm_nin_verification(nin):
    url = "/identity/v2/validate"
    payload = {
        "type": "NIN",
        "async": False,
        "number": nin,
        "debitAccountNumber": "000xxxxxxx",
    }
    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        if response["statusCode"] != 200:
            return [False, response.get("data")["_id"]]
        return [True, response.get("data")["_id"]]

    except Exception as error:
        print(error)
        return {"error": "Could not create account"}
