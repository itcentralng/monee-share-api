from fastapi import FastAPI
from sms import controller as sms_controller
from sms.model import SMSModel
from templates.response_templates import (
    AccountResponses,
    FormatResponses,
    Responses,
    TransferResponses,
)
import logging
from call import controller as call_controller
from commands import controller as command_controller


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)


app = FastAPI()
app.include_router(
    call_controller.router,
    prefix="/call",
    tags=["call"],
)


@app.get("/")
async def index():
    return {"app": "Monee Share", "status": "ok"}


@app.post("/sms")
async def receive_sms(sms: SMSModel):
    user_phone = sms.from_
    command_str = sms.text.lower()
    print("user query: " + command_str)

    if not len(command_str):
        await sms_controller.send_sms(FormatResponses.NO_COMMAND_FOUND, [user_phone])
        return {"message": FormatResponses.NO_COMMAND_FOUND}

    user_query_list = command_str.split(" ")
    command = user_query_list[0]

    ####################################
    # COMMANDS WITHOUT EXTRA PARAMETERS
    match command:
        case "help":
            return command_controller.help(user_phone, True)

    match command:
        case "balance":
            return await command_controller.balance(user_phone, command_str, True)

    ####################################
    # COMMANDS WITH EXTRA PARAMETERS (x1)
    if len(user_query_list) < 2:
        await sms_controller.send_sms(FormatResponses.BAD_FORMAT, [user_phone])
        return {"message": FormatResponses.BAD_FORMAT}

    # match command:
    #     case "create":
    #         await sms_controller.send_sms(Responses.SEND_CONFIRMATION, [user_phone])
    #         return {"message": AccountResponses.CREATE_SUCCESS}

    ####################################
    # COMMANDS WITH EXTRA PARAMETERS (x2)
    if len(user_query_list) < 3:
        await sms_controller.send_sms(FormatResponses.BAD_FORMAT, [user_phone])
        return {"message": FormatResponses.BAD_FORMAT}

    match command:
        case "util":
            # await sms_controller.send_sms(Responses.UTIL_CONFIRM, [user_phone])
            # response = await util_controller.util(
            #     {"user": sender_bank_account, "user_query_list": user_query_list}
            # )
            # print(response)
            # return response
            pass
        case "send":
            # await sms_controller.send_sms(Responses.SEND_CONFIRMATION, [user_phone])
            return TransferResponses.SEND_CONFIRMATION
        case _:
            # await sms_controller.send_sms(Responses.NOT_UNDERSTOOD, [user_phone])
            return FormatResponses.NOT_UNDERSTOOD
