import urllib

async def transform_request(request):
    decoded_string = await request.body()
    dictionary = urllib.parse.parse_qs(decoded_string.decode("utf-8"))
    transformed_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, list) and len(value) == 1:
            transformed_dict[key] = value[0]
        else:
            transformed_dict[key] = value
    return transformed_dict
