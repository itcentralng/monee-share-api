from urllib import response
from transactions import db
from accounts import controller as account_controller
from transactions.models import TransactionInputModel


async def get_and_perform(phone: str):
    transaction = await db.get_transaction(phone)
    response = None

    if transaction:
        text = transaction.command.lower()
        user_query_list = text.split(" ")
        command = user_query_list[0]

        print("Command: " + command)

        match transaction.command:
            case "balance":
                response = await account_controller.perform_get_balance(phone)
            case "util":
                pass
            case "send":
                pass

    return response


async def add_transaction(transation: TransactionInputModel):
    return await db.add_transaction(transation)
