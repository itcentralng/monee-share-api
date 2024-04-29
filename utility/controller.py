from pydantic import BaseModel
from templates.response_templates import Responses, UtilResponses
from utility.models import UtilParam
from . import db as database
from . import bank as haven
from accounts import controller


async def util(util: UtilParam):
    verified_meter = await verify_meter(util["user_query_list"][2])
    print(verified_meter)

    if not verified_meter:
        return UtilResponses.UTIL_CONFIRM
    else:
        return UtilResponses.UTIL_VERIFICATION_FAILED.format(
            meter_number=verified_meter.account
        )


async def verify_meter(util: UtilParam):
    meter = util
    return meter


# async def verify(data):
#     sender_account, command = data.values()
#     has_funds, balance = await account.has_funds(
#         {"account_id": sender_account["safehavenId"], "amount": command[1]}
#     )

#     # if not has_funds:
#     if False:
#         if balance is None:
#             verified_user = f"Something went wrong on our side. Please try again"
#         else:
#             response = f"Insufficient funds !.\nAccount balance: N{balance}. \nFund your account and try again"

#     else:
#         discos = await database.get_discos_by_state(command[3])
#         meter = None
#         print(discos)

#         if not len(discos):
#             return False
#         else:
#             for disco in discos:
#                 meter = await haven.verify_util(command[2], disco["safehavenId"])
#                 if "data" in meter:
#                     current_disco = disco
#                     meter = meter["data"]
#                     break
#                 else:
#                     meter = None

#             print(meter)
#             if meter:
#                 return meter
#             else:
#                 return None

#     return response


# async def buy(data):
#     sender_account, command = data.values()
#     if len(command) < 4:
#         response = f'Information provided is not formatted correctly. please send "help" for details on the command'
#     else:
#         has_funds, balance = await account.has_funds(
#             {"account_id": sender_account["safehavenId"], "amount": command[1]}
#         )

#         # if not has_funds:
#         if False:
#             if balance is None:
#                 response = f"Something went wrong on our side. Please try again"
#             else:
#                 response = f"Insufficient funds !.\nAccount balance: N{balance}. \nFund your account and try again"

#         else:
#             discos = await database.get_discos_by_state(command[3])
#             current_disco = None
#             meter = None
#             print(discos)
#             if not len(discos):
#                 response = f'Please enter a valid state name or send "help" for details on the command'
#             else:
#                 for disco in discos:
#                     meter = await haven.verify_util(command[2], disco["safehavenId"])
#                     if "data" in meter:
#                         current_disco = disco
#                         meter = meter["data"]
#                         break
#                     else:
#                         meter = None

#                 print(meter)
#                 if meter:
#                     payload = {
#                         "amount": int(command[1]),
#                         "channel": "WEB",
#                         "serviceCategoryId": current_disco["safehavenId"],
#                         "debitAccountNumber": sender_account["account"],
#                         "meterNumber": command[2],
#                         "vendType": meter["vendType"],
#                     }
#                     payment_response = await haven.pay_util(payload)
#                     print(payment_response)
#                     if not payment_response.get("data"):
#                         response = f"""Could not buy utility for\n\nName: {meter["name"]}\nAddress: {meter["address"]}\nAmount: {command[1]}\nTry again later"""
#                         print(payment_response)

#                     else:
#                         print(payment_response)
#                         payment_response = payment_response.get("data")

#                         response = f"""Utility purchase successful.\nName: {meter["name"]}\nAddress: {meter["address"]}\n\nEnter your pin to confirm\nAmount: {command[1]}\nTry again later\nToken: {payment_response.get("utilityToken")}"""

#                 else:
#                     response = f"Could not verify your utility. Check the meter number"

#     return response
