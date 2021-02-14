import json


def get_request_data(request):
    data = request.GET.dict().items()
    result = {}
    for key, value in data:
        try:
            result[key] = json.loads(value)
        except json.decoder.JSONDecodeError:
            result[key] = value
    return result
