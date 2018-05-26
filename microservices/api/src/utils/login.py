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
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+json.loads(resp.content)['auth_token'],
        "X-Hasura-Role": "admin"
    }
    return headers