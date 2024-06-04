from typing import Annotated
from fastapi import Depends, FastAPI, Form, Request
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


# def get_sms_data(
#     date: str | None = Form(default=None),
#     from_: str = Form(alias="from"),
#     id: str | None = Form(default=None),
#     linkId: str | None = Form(default=None),
#     text: str = Form(...),
#     to: str | None = Form(default=None),
#     networkCode: str | None = Form(default=None),
# ):
#     return SMSModel(
#         date=date,
#         from_=from_,
#         id=id,
#         linkId=linkId,
#         text=text,
#         to=to,
#         networkCode=networkCode,
#     )
async def get_sms_data(request: Request):
    data = await request.form()
    return SMSModel(**data._dict)


@app.post("/sms")
async def receive_sms(sms: Annotated[SMSModel, Depends(get_sms_data)]):
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
            return await command_controller.help(user_phone, command_str, True)

    match command:
        case "balance":
            return await command_controller.balance(user_phone, command_str, True)

    ####################################
    # COMMANDS WITH EXTRA PARAMETERS (x1)
    if len(user_query_list) < 2:
        await sms_controller.send_sms(FormatResponses.BAD_FORMAT, [user_phone])
        return {"message": FormatResponses.BAD_FORMAT}

    match command:
        case "create":
            return await command_controller.create(user_phone, user_query_list, True)

    ####################################
    # COMMANDS WITH EXTRA PARAMETERS (x2)
    if len(user_query_list) < 3:
        await sms_controller.send_sms(FormatResponses.BAD_FORMAT, [user_phone])
        return {"message": FormatResponses.BAD_FORMAT}

    match command:
        case "send":
            return await command_controller.transfer_funds(
                user_phone, user_query_list, True
            )

    ####################################
    # COMMANDS WITH EXTRA PARAMETERS (x4)
    if len(user_query_list) < 4:
        await sms_controller.send_sms(FormatResponses.BAD_FORMAT, [user_phone])
        return {"message": FormatResponses.BAD_FORMAT}

    match command:
        case "util":
            return await command_controller.util(user_phone, user_query_list, True)
        case _:
            await sms_controller.send_sms(FormatResponses.NOT_UNDERSTOOD, [user_phone])
            return FormatResponses.NOT_UNDERSTOOD
