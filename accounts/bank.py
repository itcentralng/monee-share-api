from lib.haven import safehaven_client


async def get_accounts():

    url = "/accounts?limit=100&isSubAccount=true"

    try:
        response = await safehaven_client.get(url)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not get accounts"}


async def get_account(account_id):
    print(account_id)

    url = f"/accounts/{account_id}"

    try:
        response = await safehaven_client.get(url)
        return response

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
