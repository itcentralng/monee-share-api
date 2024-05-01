from templates.response_templates import UtilResponses
from utility.models import UtilModel, UtilParam
from utility import db as database
from utility import bank as haven
from accounts import controller as account_controller
from messages import controller as message_controller


async def verify_meter(util: UtilParam):
    discos = await database.get_discos_by_state(util["user_query_list"][3])
    meter = None
    disco = None

    print(discos)
    if not len(discos):
        return meter
    else:
        for d in discos:
            temp = await haven.verify_util(util["user_query_list"][2], d["safehavenId"])
            if "data" in temp:
                meter = temp["data"]
                disco = d
                break

    if meter:
        print(meter)
        print(f'Disco: {disco["name"]}\nMeter number: {meter["meterNo"]}')
        return UtilModel(
            **meter,
            categoryId=disco["safehavenId"],
            disco=disco["name"],
        )
    else:
        return meter


async def perform_pay_util(user_phone: str, user_query_list: str):
    user_db_account = await account_controller.get_account_from_db(user_phone)
    user_bank_account = await account_controller.get_account_from_haven(
        user_db_account.safehavenId
    )

    verified_meter = await verify_meter(
        {
            "user": user_db_account,
            "user_query_list": user_query_list,
        }
    )

    payload = {
        "amount": int(user_query_list[1]),
        "channel": "WEB",
        "serviceCategoryId": verified_meter.categoryId,
        "debitAccountNumber": user_bank_account.accountNumber,
        "meterNumber": user_query_list[2],
        "vendType": verified_meter.vendType,
    }
    payment_response = await haven.pay_util(payload)

    print(payment_response)
    if "error" in payment_response or (
        "statusCode" in payment_response and payment_response["statusCode"] == 400
    ):
        bot_message = {
            "content": UtilResponses.UTIL_PURCHASE_FAILED,
            "role": "bot",
            "phone": user_db_account.phone,
        }
        await message_controller.add_message(bot_message)
        return {"message": UtilResponses.UTIL_PURCHASE_FAILED}
    else:
        payment_response = payment_response["data"]
        bot_message = {
            "content": UtilResponses.UTIL_PURCHASE_SUCCESS.format(
                token=payment_response["utilityToken"],
                amount=payment_response["amount"],
            ),
            "role": "bot",
            "phone": user_db_account.phone,
        }
        await message_controller.add_message(bot_message)
        return {
            "message": UtilResponses.UTIL_PURCHASE_SUCCESS.format(
                token=payment_response["utilityToken"],
                amount=payment_response["amount"],
            )
        }
