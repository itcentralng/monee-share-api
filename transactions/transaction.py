from . import db as database
from . import bank as haven
from accounts import account
from lib.sms import AfricasTalking
from messages import db as msg_database
from transactions import db as transaction_db

af_sms = AfricasTalking()


async def send(data):
    global responses
    (sender_account, command) = data.values()

    has_funds, balance = await account.has_funds(
        {"account_id": sender_account.get("safehavenId"), "amount": command[1]}
    )
    # if not has_funds:
    if False:
        response = f"Insufficient funds !.\nAccount balance: N{balance}. \nFund your account and try again"
    else:
        receiver_account_db = await account.get_account_from_db({"phone": command[2]})

        if not receiver_account_db.get("_id"):
            receiver_account = await account.create(
                {"sender": command[2], "command": command}
            )

            if receiver_account.get("_id"):
                response = f"""Welcome to Monee Share
                    Your account was created successfully.
                    Use your phone number to send/receive money on Monee Share

                    to fund your account from other banks use:
                    Account Number: {receiver_account["accountNumber"]}
                    Bank: Safehaven MFB

                    For more information, send help"
                """
                # SEND MESSAGE TO RECEIVER ON ACCOUNT CREATION
                af_sms.send(response, [command[2]])
                await msg_database.add_message(
                    {
                        "phone": command[2],
                        "role": "bot",
                        "content": response,
                    }
                )

                # SEND MESSAGE TO SENDER ON ACCOUNT CREATION
                response = f"Account created for {command[2]}"
                af_sms.send(
                    response,
                    [sender_account.get("phone")],
                )
                await msg_database.add_message(
                    {
                        "phone": sender_account.get("phone"),
                        "role": "bot",
                        "content": response,
                    }
                )

            else:
                af_sms.send(receiver_account, [command[2]])
                await msg_database.add_message(
                    {
                        "phone": sender_account.get("phone"),
                        "role": "bot",
                        "content": receiver_account,
                    }
                )
        else:
            receiver_account = await account.get_account_from_haven(
                {"account_id": receiver_account_db.get("safehavenId")}
            )
            receiver_account = receiver_account.get("data")

        receiver_name = (
            receiver_account.get("accountName")
            .lower()
            .replace("itcentrallimite / customer_", "")
        )

        response = f"You are sending N{command[1]}\nto {receiver_name}.\n\nYou will get a call from us to enter your pin for confirmation"

        payload = {
            "command": " ".join(command),
            "status": "pending",
            "type": "transfer",
            "user": sender_account.get("phone"),
        }

        await transaction_db.add_transaction(payload)

    return response


async def make_transfer(sender_account, command):
    beneficiary = await account.get_account_from_db({"phone": command[2]})
    response = None
    status = None

    if beneficiary.get("account"):
        banks = await haven.get_banks()
        bank = None
        for bnk in banks.get("data"):
            if "safe haven sandbox bank" in bnk.get("name").lower():
                bank = bnk
                break

        payload = {
            "bankCode": bank["bankCode"],
            "accountNumber": beneficiary["account"],
        }

        name_enquiry = await haven.name_enquiry(payload)

        if name_enquiry.get("data"):
            name_enquiry = name_enquiry.get("data")

            payload = {
                "saveBeneficiary": False,
                "nameEnquiryReference": name_enquiry["sessionId"],
                "beneficiaryBankCode": bank["bankCode"],
                "debitAccountNumber": sender_account["account"],
                "beneficiaryAccountNumber": beneficiary["account"],
                "amount": command[1],
            }
            transaction_response = await haven.make_transfer(payload)
            if transaction_response.get("data"):
                response = f"You successfully sent N{command[1]} to {command[2]}"
                status = "ok"
                af_sms.send(response, [sender_account.get("phone")])

                beneficiary_account = await account.get_account_from_haven(
                    {"account_id": beneficiary.get("safehavenId")}
                )
                receiver_response = f'You received N{command[1]} from {sender_account.get("firstName")}.\n\nYour new balance: N{beneficiary_account.get("data")["accountBalance"]}'
                af_sms.send(receiver_response, [beneficiary.get("phone")])
            else:
                response = f"There was a problem sending N{command[1]} to {command[2]}. Try again"
                af_sms.send(response, [beneficiary.get("phone")])
                status = "failed"
        else:
            status = "failed"
            response = f"Name enquiry was not successfull"
    else:
        status = "failed"
        response = f"Could not find beneficiary's account"

    return [response, status]


async def buy_util():
    pass
