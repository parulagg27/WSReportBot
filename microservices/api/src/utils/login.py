import requests
import json

def login(username,password):
    url = "https://auth.graveside44.hasura-app.io/v1/login"
    requestPayload = {
        "provider": "username",
        "data": {
            "username": username,
            "password": password
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    # print(str(resp.content.decode('utf-8')))
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+str(json.loads(resp.content.decode('utf-8'))['auth_token']),
        "X-Hasura-Role": "admin"
    }
    return headers