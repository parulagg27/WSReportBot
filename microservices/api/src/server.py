import os
import json
import signal
import requests
import subprocess
from src import app
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from src.utils.login import login
from flask import jsonify, request
from flask import Flask, render_template
from src.utils.backend import get_weekly_report, get_language_report_week

slackToken = "wk6GW3p1fzUbC7gNHbgxtsYa"
# slackToken = os.environ['SLACK_TOKEN']
botAccessToken = "xoxb-374384770263-374217359473-SfFw7D91EQWKz5qaxfS1hJVZ"
# botAccessToken = os.environ['BOT_ACCESS_TOKEN']
hasuraDataUrl = "http://data.hasura/v1/query"
chatUrl = "https://slack.com/api/chat.postMessage"

headers = login('mehul','mehul@hasura')
p = None

def sendConfirmation(id, message, responseUrl):
    payload = {
        "text": "Showing You reports for last week",
        "attachments": [
            {
                "text": '"'+message+'"',
                "fallback": "You are indecisive",
                "callback_id": id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "yes",
                        "text": "Yep",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "no",
                        "text": "Nope",
                        "type": "button",
                        "value": "no"
                    }
                ]
            }
        ]
    }
    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", responseUrl, data=json.dumps(payload), headers=headers)
    print(response.text)


@app.route("/")
def home():
    return "Hello Parul :P"

@app.route('/langslack', methods=['POST'])
def event():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        id = "None"
        sendConfirmation(id, receivedMessage, data["response_url"])
        return "Waiting for confirmation"
    else:
        return "Invalid Token"

@app.route('/reportslack', methods=['POST'])
def event():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        org_name = receivedMessage
        user_report, date = get_weekly_report(org_name = org_name,headers = headers)
        return "Waiting for confirmation"
    else:
        return "Invalid Token"


@app.route("/login")
def chk_login():
    headers = login('mehul','mehul@hasura')
    return "Hello Parul :P"

@app.route("/start")
def start():
    global p
    p = subprocess.Popen(["python","src/utils/clock.py"])
    return "Hello Parul :P"

@app.route("/kill")
def kill():
    global p
    p.kill()
    return "Hello Parul :P"

@app.route("/report/<org_name>")
def report(org_name):
    # T = datetime(month=5,day=15,year=2018)
    # user_report, date = get_weekly_report(org_name = org_name,headers = headers,day = T)
    user_report, date = get_weekly_report(org_name = org_name,headers = headers)
    return render_template("cards.html",user_report=user_report, date=date)

@app.route("/lang")
def language_report():
    # T = datetime(month=5,day=15,year=2018)+timedelta(days=7)
    # lang_report = get_language_report_week(headers = headers, day = T)
    lang_report = get_language_report_week(headers = headers)
    return render_template("lang.html",lang_report = lang_report)

@app.route("/json")
def json_message():
    return jsonify(message="Hello World")



'''
# To add a project call from utils/project_init.py 
headers = login('mehul','mehul@hasura') 
main('mulx10','OpenGenus','cosmos',headers)
'''