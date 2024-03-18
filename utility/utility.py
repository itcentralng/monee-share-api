from . import db as database
from . import bank as haven
from accounts import account


async def buy(data):
    sender_account, command = data.values()
    if len(command) < 4:
        response = f'Information provided is not formatted correctly. please send "help" for details on the command'
    else:
        has_funds, balance = await account.has_funds(
            {"account_id": sender_account["safehavenId"], "amount": command[1]}
        )

        # if False:
        if not has_funds:
            response = f"Insufficient funds !.\nAccount balance: N{balance}. \nFund your account and try again"
        else:
            discos = await database.get_discos_by_state(command[3])
            current_disco = None
            meter = None
            print(discos)
            if not len(discos):
                response = f'Please enter a valid state name or send  help" for details on the command'
            else:
                for disco in discos:
                    meter = await haven.verify_util(command[2], disco["safehavenId"])
                    if "data" in meter:
                        current_disco = disco
                        meter = meter["data"]
                        break
                    else:
                        meter = None

                print(meter)
                if meter:
                    response = f"""Name: {meter["name"]}\nAddress: {meter["address"]}\n\nEnter your pin to confirm\nAmount: {command[1]}"""
                    payload = {
                        "amount": int(command[1]),
                        "channel": "WEB",
                        "serviceCategoryId": current_disco["safehavenId"],
                        "debitAccountNumber": sender_account["account"],
                        "meterNumber": command[2],
                        "vendType": meter["vendType"],
                    }
                    payment_response = await haven.pay_util(payload)
                    print(payment_response)
                    if not payment_response.get("data"):
                        print(payment_response)
                        response = f"Could not buy utility. Try again later"
                    else:
                        print(payment_response)
                        response = f"payment successfull"

                else:
                    response = f"Could not verify your utility. Check the meter number"

    return response
