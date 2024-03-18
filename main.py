import os
from dotenv import load_dotenv
from convex import ConvexClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel

# from fastapi.responses import PlainTextResponse
from utils.functions import transform_request
from utils.sms import AfricasTalking
from utils.haven import SafeHaven
from utils.db import DB
import sync_db
import convex_route

load_dotenv()
app = FastAPI()
haven = SafeHaven()
database = DB()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sync_db.router, prefix="/sync")
app.include_router(convex_route.router, prefix="/convex")


CONVEX_URL = os.environ.get("CONVEX_URL")

convex_client = ConvexClient(os.environ.get("CONVEX_URL"))

ACCERTION = os.environ.get("SAFEHAVEN_ACCERTION")
print(ACCERTION)


@app.get("/")
async def home():
    return {"app": "Money share", "status": "ok"}


@app.post("/sms")
async def receive_sms(request: Request):
    request = await transform_request(request)
    msg = request.get("text", None)
    to = request.get("to", None)
    sender = request.get("from", None)
    # date = request["date"]

    command = msg.split()
    print(command)

    response = ""
    db_account = await database.get_account(sender)

    # HELP
    if "help" in msg:
        response = f"""List of commands:\n1. create -> mshare create [NIN/BVN]\n2. send -> mshare send [AMOUNT] [PHONE_NUMBER]\n3. util -> mshare util [AMOUNT] [METER_NUM] [STATE]\n4. balance -> mshare balance\n5. help -> mshare help"""
    # END OF HELP

    elif not len(db_account) and "create" not in msg:
        response = f"""It seems you don't have an account. Send "mshare create NIN/BVN" to 9011 to create your account."""

    elif len(db_account) and "create" in msg:
        response = f"""It seems you already have an account. Send "mshare help" to 9011 for more information."""

    # BALANCE
    elif "balance" in msg:
        print(db_account[0]["safehavenId"])
        account = await haven.get_account(db_account[0]["safehavenId"])

        if "data" in account:
            response = f'Your balance is N{account["data"]["accountBalance"]}'
        else:
            response = f"Could not get your account balance. Please try again"
    # END OF BALANCE

    elif len(command) < 3:
        response = f'Not enough information provided. please send "help" to 9011 for details on the command'

    # START OF CREATE
    elif "create" in msg:
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
                "nin": command[2],
            }

            db_response = await database.create_account(payload)
            print(db_response)

            response = f"""Welcome to Monee Share
                Your account was created successfully.
                Use your phone number to send/receive money on Monee Share

                to fund your account from other banks use: 
                Account Number: {account["accountNumber"]}
                Bank: Safehaven MFB

                For more infotmation, send "mshare help" to 9011
            """

    # END OF CREATE

    # UTIL
    elif "util" in msg:
        if len(command) != 5:
            response = f'Information provided is not formatted correctly. please send "help" to 9011 for details on the command'
        else:
            has_funds, balance = await haven.has_funds(
                db_account[0]["safehavenId"], command[2]
            )

            # if not has_funds:
            #     response = f"Insufficient funds !.\nAccount balance: N{balance}. Fund your account and try again"
            if False:
                response = f"Insufficient funds !.\nAccount balance: N{balance}. Fund your account and try again"
            else:
                discos = await database.get_discos_by_state(command[4])
                current_disco = None
                meter = None
                print(discos)
                if not len(discos):
                    response = f'Please enter a valid state name or send "mshare help" to 9011 for details on the command'
                else:
                    for disco in discos:
                        meter = await haven.verify_util(
                            command[3], disco["safehavenId"]
                        )
                        if "data" in meter:
                            current_disco = disco
                            meter = meter["data"]
                            break
                        else:
                            meter = None

                    print(meter)
                    if meter:
                        response = f"""Name: {meter["name"]}\nAddress: {meter["address"]}\n\nEnter your pin to confirm\nAmount: {command[2]}"""
                        payload = {
                            "amount": command[2],
                            "channel": "WEB",
                            "serviceCategoryId": current_disco["safehavenId"],
                            "debitAccountNumber": db_account[0]["account"],
                            "meterNumber": command[3],
                            "vendType": meter["vendType"],
                        }
                        # payment_response = await haven.pay_util(payload)
                        # print(payment_response)
                        # if not payment_response.get("data"):
                        #     print(payment_response)
                        #     response = f"Could not buy utility. Try again later"

                    else:
                        response = (
                            f"Could not verify your utility. Check the meter number"
                        )
    # END OF UTIL

    # TRANSFER
    elif "send" in msg:
        banks = await haven.get_banks()
        for bank in banks.get("data"):
            if "safe haven sandbox bank" in bank.get("name").lower():
                print(bank)
                payload = {
                    "bankCode": bank["bankCode"],
                    "accountNumber": db_account["account"],
                }
                print(payload)
                # name_enquiry = await haven.name_enquiry(bank[""])

        response = f"Sent xxxxx to +234xxx successfully"
    else:
        response = (
            f'Command not understood.\nText "help" to 9011 for the list of all commands'
        )
    # END OF TRANSFER

    print(response, sender)
    AfricasTalking.send(AfricasTalking, response, [sender], to)


@app.post("/call")
async def receive_call(request: Request):
    print(await request.body())
