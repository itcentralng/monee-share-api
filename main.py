import os
from dotenv import load_dotenv
from convex import ConvexClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
# from fastapi.responses import PlainTextResponse
from utils.functions import transform_request
from utils.africastalking import AfricasTalking
from utils.haven import SafeHaven
from utils.db import DB
import sync_db

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
        response = f"""List of commands:
            1. create -> Mshare create [NIN/BVN]
            2. send -> Mshare send [AMOUNT] [PHONE_NUMBER]
            3. util -> Mshare util [AMOUNT] [METER_NUM] [STATE]
            4. balance -> Mshare balance
            5. help -> Mshare help
        """
    # END OF HELP
        
    elif not len(db_account):
        response = f"""It seems you don't have an account. Send "create NIN/BVN" to 9011 to create your account."""

    # BALANCE
    elif "balance" in msg:
        print(db_account[0]["safehavenId"])
        account = await haven.get_account(db_account[0]["safehavenId"])

        if "data" in account:
            response = f'Your balance is N{account["data"]["accountBalance"]}'
        else:
            response = f'Could not get your account balance. Please try again'
    # END OF BALANCE
            
    elif len(command) < 3:
        response = f'Not enough information provided. please send "help" to 9011 for details on the command'

    # START OF CREATE
    elif "create" in msg:
        payload = {
            "firstName": f"customer_{sender.replace("+","")}",
            "phoneNumber": sender,
            "emailAddress": f"customer_{sender.replace("+","")}@moneeshare.com",
            "externalReference": f"{sender.replace("+","")}",
        }
        account = await haven.create_account(payload)
        print(account)

        if not account.get("data",None):
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
            "nin": command[2]
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
            has_funds, balance = await haven.has_funds(db_account[0]["safehavenId"], command[2])

            # if not has_funds:
            #     response = f"No sufficient funds !.\nAccount balance: N{balance}. Fund your account and try again" 
            if False:
                response = f"Insufficient funds !.\nAccount balance: N{balance}. Fund your account and try again" 
            else:
                discos = await database.get_discos_by_state(command[4])
                meter = None
                print(discos)
                if not len(discos):
                    response = f'Please enter a valid state name or send "help" to 9011 for details on the command'
                else:
                    for disco in discos:
                        meter = await haven.verify_util(command[3], disco["safehavenId"])
                        if "data" in meter:
                            break
                        else:
                            meter = None
                            
                    print(meter)
                    if meter:
                        response = f"""Name: {meter["data"]["name"]}\nAddress: {meter["data"]["address"]}\n\nEnter your pin to confirm\nAmount: {command[2]}"""
                    else:
                        response = f"Could not verify your utility. Check the meter number"                      
    # END OF UTIL
    elif "send" in msg:
        response = f"Sent xxxxx to +234xxx successfully"
    else:
        response = f'Command not understood.\nText "help" to 9011 for the list of all commands'

    print(response)
    AfricasTalking.send(AfricasTalking, response, [sender], to)
