from fastapi import Request, FastAPI, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from accounts import account as account_controller
from utility import utility
from transactions import transaction
from messages import db as msg_database
import lib.signalwire as signalwire
from transactions import db as transaction_db
from lib.sms import AfricasTalking


load_dotenv()
app = FastAPI()


@app.post("/sms")
async def receive_sms(request: Request):
    resp = await request.form()
    Body = resp.get("Body")
    From = resp.get("From")
    AF_number = resp.get("to")

    print(resp)
    if not Body:
        From = resp.get("from")
        Body = resp.get("text")

    Body = Body.lower()
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
        print(payload)
        await transaction_db.add_transaction(payload)
        # signalwire.make_call(From)

    # END OF UTIL

    # TRANSFER
    elif "send" in Body and "error" not in sender_account:
        response = await transaction.send(
            {
                "sender": From,
                "sender_account": sender_account,
                "command": command,
                "msg": Body,
                "AF_NUMBER": AF_number,
                "From": From,
            }
        )

        payload = {
            "command": Body,
            "status": "pending",
            "type": "send",
            "user": From,
        }
        print(payload)
        await transaction_db.add_transaction(payload)

        signalwire.make_call(From)

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

    # SEND MESSAGE IF MESSAGE IS FROM AFRICASTALKING
    if AF_number:
        af_sms = AfricasTalking()
        af_sms.send(response, [From], AF_number)

    msg_res = MessagingResponse()
    msg_res.message(response)
    return Response(content=str(msg_res), media_type="application/xml")


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

    response = VoiceResponse()
    print(req)

    if digits:
        response.say("thank you. Your transaction will be processed")
        is_valid_pin = await account_controller.verify_pin(digits)
        if is_valid_pin:
            # process transaction
            transct = await transaction_db.get_transaction({"phone": req.get("From")})
            await receive_sms(
                {"From": transct.get("user"), "Body": transct.get("command")}
            )
    else:
        response.say("Invalid input. Please try again.")

    return Response(content=response.to_xml(), media_type="text/xml")


@app.get("/sync")
async def sync():
    from lib.sync_db import sync_users

    await sync_users()
    return {"message": "successful"}
