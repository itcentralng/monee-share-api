from utils.haven import safehaven_client


async def get_services():

    url = "/vas/services"

    try:
        response = await safehaven_client.get(url)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not get services"}


async def get_categories(service_id):

    url = f"/vas/service/{service_id}/service-categories"

    try:
        response = await safehaven_client.get(url)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not get categories"}


async def verify_util(meter_number, service_id):

    url = "/vas/verify"
    payload = {"entityNumber": meter_number, "serviceCategoryId": service_id}

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not verify util"}


async def pay_util(payload):

    url = "/vas/pay/utility"

    try:
        response = await safehaven_client.post(url, payload, has_token=True)
        return response

    except Exception as error:
        print(error)
        return {"error": "Could not pay for util"}
