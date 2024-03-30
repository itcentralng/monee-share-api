import os
from fastapi import Request, FastAPI, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from accounts import account as account_controller
from utility import utility
from transactions import transaction
from messages import db as msg_database
import lib.sigwire as sigwire
from transactions import db as transaction_db
from lib.sms import AfricasTalking
import logging
from starlette.datastructures import FormData


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


load_dotenv()
app = FastAPI()
af_sms = AfricasTalking()
af_number = os.environ.get("AFRICASTALKING_SENDER")


@app.get("/")
async def index():
    return {"app": "Monee Share", "status": "ok"}


@app.post("/sms")
async def receive_sms(request: Request):
    if isinstance(request, FormData):
        req = dict(request)
    else:
        req = await request.form()

    Body = req.get("Body")
    From = req.get("From")
    AF_number = req.get("to")

    print(req)
    if not Body:
        From = req.get("from")
        Body = req.get("text")

    Body = Body.lower()
    Body = Body.replace("mshare", "")
    command = Body.split()

    response = ""
    sender_account = await account_controller.get_account_from_db({"phone": From})
    print(command, From)
    print(sender_account)

    # INSERT MESSAGE INTO DATABASE
    await msg_database.add_message(
        {
            "phone": From,
            "role": "user",
            "content": Body,
        }
    )

    # HELP
    if "help" in Body:
        response = f"""List of commands:\n1. create -> create [NIN/BVN]\n2. send -> send [AMOUNT] [PHONE_NUMBER]\n3. util -> util [AMOUNT] [METER_NUM] [STATE]\n4. balance -> balance\n5. help -> help"""
    # END OF HELP

    elif "error" in sender_account and "create" not in Body:
        response = f"""It seems you don't have an account. Send create NIN/BVN" to create your account."""

    elif "error" not in sender_account and "create" in Body:
        response = f"""It seems you already have an account.\nSend "help" for more information."""

    # BALANCE
    elif "balance" in Body and "error" not in sender_account:
        response = await account_controller.get_balance(
            {"sender_account": sender_account}
        )
    # END OF BALANCE

    elif len(command) < 3 and "create" not in Body:
        response = f'Not enough information provided. please send "help" for details on the command'

    # START OF CREATE
    elif "create" in Body:
        response = await account_controller.create({"sender": From, "command": command})
        if response.get("_id"):
            response = f'Welcome to Monee Share.\nYour account was created successfully.\nUse your phone number to send/receive money on Monee Share.\n\nto fund your account from other banks use:\nAccount Number: {response.get("accountNumber")}.\nBank: Safehaven MFB.\n\nFor more information, send "help" to {af_number}'

    # END OF CREATE

    # UTIL
    elif "util" in Body and "error" not in sender_account:
        response = await utility.buy(
            {"sender_account": sender_account, "command": command}
        )

        payload = {
            "command": Body,
            "status": "pending",
            "type": "send",
            "user": From,
        }
        # print(payload)

        # await transaction_db.add_transaction(payload)
        # make call

    # END OF UTIL

    # TRANSFER
    elif "send" in Body and "error" not in sender_account:
        response = await transaction.send(
            {
                "sender_account": sender_account,
                "command": command,
            }
        )

        sigwire.make_call(From)

    else:
        response = f'Command not understood.\nText "help" for the list of all commands'
    # END OF TRANSFER

    # INSERT MESSAGE INTO DATABASE
    await msg_database.add_message(
        {
            "phone": From,
            "role": "bot",
            "content": response,
        }
    )
    print(response)

    # SEND MESSAGE
    af_sms.send(response, [From])


@app.post("/call_receiver")
def call_receiver(request: Request):
    response = VoiceResponse()
    gather = Gather(action=request.url_for("call_handler"), method="POST", numDigits=4)
    gather.say("Welcome! Please dial in your pin number, to confirm transaction.")

    response.append(gather)
    response.say("We did not receive any input. Goodbye!")

    return Response(response.to_xml(), mimetype="text/xml")


@app.post("/call")
async def call_handler(request: Request):
    req = await request.form()
    digits = req.get("Digits")
    From = req.get("From")
    response = VoiceResponse()

    sender_account = await account_controller.get_account_from_db({"phone": From})
    if not sender_account.get("_id"):
        response.say(
            f"It seems you don't have an account. send help to {' '.join(af_number.split())}"
        )
        return Response(content=response.to_xml(), media_type="text/xml")

    if digits:
        is_valid_pin = await account_controller.verify_pin(
            {"phone": From, "pin": digits}
        )
        if is_valid_pin:
            transct = await transaction_db.get_transaction({"phone": From})
            transaction_type = transct.get("type")
            response.say("thank you. Your transaction will be processed")
            response.hangup()

            if transaction_type == "transfer":
                trasaction_response, transaction_status = (
                    await transaction.make_transfer(
                        sender_account, transct.get("command").split()[2]
                    )
                )
                print(trasaction_response)
            elif transaction_type == "util":
                # handle utility
                # verify meter number
                # check balance
                # proceed with payment
                pass

        else:
            response.say("Your pin is incorrect. confirm the pin and try again")
    else:
        response.say("Invalid input. Please try again.")

    return Response(content=response.to_xml(), media_type="text/xml")


@app.get("/sync")
async def sync():
    from lib.sync_db import sync_users

    await sync_users()
    return {"message": "successful"}
