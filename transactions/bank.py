from lib._safehaven import safehaven_client


async def name_enquiry(payload):

    url = "/transfers/name-enquiry"

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not enquire name"}


async def get_banks():

    url = "/transfers/banks"

    try:
        response = await safehaven_client.get(url)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not fetch banks"}


async def make_transfer(payload):

    url = "/transfers"

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not make transfer"}
