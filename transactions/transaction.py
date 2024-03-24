from . import db as database
from . import bank as haven
from accounts import account
from lib.sms import AfricasTalking
from messages import db as msg_database


async def send(data):
    (sender, sender_account, command, msg, AF_number, From) = data.values()
    print(sender_account["safehavenId"])
    has_funds, balance = await account.has_funds(
        {"account_id": sender_account["safehavenId"], "amount": command[1]}
    )

    # if not has_funds:
    if False:
        if balance is None:
            response = f"Something went wrong on our side. Please try again"
        else:
            response = f"Insufficient funds !.\nAccount balance: N{balance}. \nFund your account and try again"

        # SEND MESSAGE IF MESSAGE IS FROM AFRICASTALKING
        if AF_number:
            af_sms = AfricasTalking()
            af_sms.send(response, [From], AF_number)

    else:
        banks = await haven.get_banks()
        for bank in banks.get("data"):
            if "safe haven sandbox bank" in bank.get("name").lower():
                beneficiary = await account.get_account_from_db({"phone": command[2]})
                print(beneficiary)

                if beneficiary.get("account"):
                    payload = {
                        "bankCode": bank["bankCode"],
                        "accountNumber": beneficiary["account"],
                    }
                    name_enquiry = await haven.name_enquiry(payload)
                    print(name_enquiry)

                    if name_enquiry.get("data"):
                        name_enquiry = name_enquiry.get("data")
                        account_name = name_enquiry["accountName"].replace(
                            "ITCENTRALLIMITE / ", ""
                        )

                        response = f"You are sending N{command[1]}\nto {account_name}\n\nYou will get a call from us to enter your pin for confirmation"

                        # # SEND MONEY
                        # payload = {
                        #     "saveBeneficiary": True,
                        #     "nameEnquiryReference": name_enquiry["sessionId"],
                        #     "debitAccountNumber": sender_account["account"],
                        #     "beneficiaryBankCode": bank["bankCode"],
                        #     "beneficiaryAccountNumber": beneficiary.get("account"),
                        #     "amount": int(command[1]),
                        # }
                        # transfer_response = await haven.make_transfer(payload)
                        # print(transfer_response)

                        # if transfer_response.get("statusCode") == 400:
                        #     print(transfer_response.get("message"))
                        #     response = transfer_response.get("message")
                        # else:
                        #     payload = {
                        #         "command": msg,
                        #         "status": transfer_response.get("data")["status"],
                        #         "type": "transfer",
                        #         "user": sender_account["_id"],
                        #         "data"
                        #         "sessionId": transfer_response.get("data")["sessionId"],
                        #     }
                        #     await database.add_transaction(payload)
                        #     response = (
                        #         f"successfully sent N{command[1]} to {account_name}"
                        #     )

                else:
                    response = await account.create(
                        {"sender": command[2], "command": command}
                    )
                    # SEND MESSAGE IF MESSAGE IS FROM AFRICASTALKING
                    if AF_number:
                        af_sms = AfricasTalking()
                        af_sms.send(
                            f"Account created for {command[2]}", [From], AF_number
                        )
                    await msg_database.add_message(
                        {
                            "phone": From,
                            "role": "bot",
                            "content": response,
                        }
                    )

                    response = f"""Welcome to Monee Share
                        Your account was created successfully.
                        Use your phone number to send/receive money on Monee Share

                        to fund your account from other banks use:
                        Account Number: {account["accountNumber"]}
                        Bank: Safehaven MFB

                        For more information, send help"
                    """
                    await msg_database.add_message(
                        {
                            "phone": command[2],
                            "role": "bot",
                            "content": response,
                        }
                    )
                    if AF_number:
                        af_sms = AfricasTalking()
                        af_sms.send(response, [command[2]], AF_number)

                    print(response)

                    beneficiary = await account.get_account_from_db(
                        {"phone": command[2]}
                    )
                    print(beneficiary)

                    if beneficiary.get("account"):
                        payload = {
                            "bankCode": bank["bankCode"],
                            "accountNumber": beneficiary["account"],
                        }

                        name_enquiry = await haven.name_enquiry(payload)
                        print(name_enquiry)

                        if name_enquiry.get("data"):
                            name_enquiry = name_enquiry.get("data")
                            beneficiary = await account.get_account_from_db(
                                {"phone": command[2]}
                            )
                            print(beneficiary)

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
                            else:
                                response = f"There was a problem sending N{command[1]} to {command[2]}. Try again"
    return response
