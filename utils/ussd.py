
# response = ""
# @app.post("/ussd", response_class=PlainTextResponse)
# async def ussd(request: Request):
#     global response
#     print(await request.body())
#     request = await transform_request(request)
#     print(request)
    
#     session_id = request.get("sessionId", None)
#     service_code = request.get("serviceCode", None)
#     phone_number = request.get("phoneNumber", None)
#     text = request.get("text", "")

#     if text == '':
#         response  = "CON Enter your pin below to confirm transaction"
#     elif text:
#         response = "END Thank you. Your transaction is being processed "
    
#     print(response)
#     return response