import requests
import json
import os
def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    print(api_key)
    print(url)
    payload = {
        "service_id" : "DOWELL10009"
    }

    response = requests.post(url, json=payload)
    print("response.status === ", response.status_code)
    print("response === ", response.text)
    # if response.status_code == 400 or response.status_code == "400":
        # raise CustomError
    # else:

    # response.status_code
    res = json.loads(response.text)
    print("res.success",res["success"])
    print("res.success type",type(res["success"]))
    return response