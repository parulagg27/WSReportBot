import os
import json
import signal
import requests
import subprocess
from src import app
from copy import copy
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from src.utils.login import login
from flask import jsonify, request
from flask import Flask, render_template
from src.utils.utils import sendSlackReport,sendSlackLangReport
from src.utils.backend import get_weekly_report, get_language_report_week

slackToken = "wk6GW3p1fzUbC7gNHbgxtsYa"
# slackToken = os.environ['SLACK_TOKEN']
botAccessToken = "xoxb-374384770263-374217359473-SfFw7D91EQWKz5qaxfS1hJVZ"
# botAccessToken = os.environ['BOT_ACCESS_TOKEN']
hasuraDataUrl = "http://data.hasura/v1/query"
chatUrl = "https://slack.com/api/chat.postMessage"

headers = login('mehul','mehul@hasura')
p = None


@app.route("/")
def home():
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

@app.route('/reportslack', methods=['POST'])
def report():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    channel =  data["channel_id"]
    if (receivedToken==slackToken):
        org_name = data["text"].strip(' ')
        user_report, date = get_weekly_report(org_name = org_name,headers = headers)
        return sendSlackReport(user_report,channel,date)
    else:
        return "Invalid Token"

@app.route('/langslack', methods=['POST'])
def lang():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    channel =  data["channel_id"]
    if (receivedToken==slackToken):
        receivedMessage= data["text"]
        lang_report = get_language_report_week(headers = headers)
        # print(lang_report)
        return sendSlackLangReport(lang_report,channel)
    else:
        return "Invalid Token"

@app.route('/init', methods=['POST'])
def init():
    data = request.form.to_dict()
    print(data)
    print("SlackToken: " + slackToken)
    receivedToken = data["token"]
    print("ReceivedToken: " + receivedToken)
    channel =  data["channel_id"]
    if (receivedToken==slackToken):
        org_name, project = data["text"].strip(' ').split(' ')
        p = subprocess.Popen(["python","src/utils/project_init.py",org_name,project])
        return "Initiating ur project :hugging_face: \n This will take time :blush:"
    else:
        return "Invalid Token"



@app.route("/report/<org_name>")
def report_ui(org_name):
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

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")

# @app.route("/login")
# def chk_login():
#     headers = login('mehul','mehul@hasura')
#     return "Hello Parul :P"



'''
# To add a project call from utils/project_init.py 
headers = login('mehul','mehul@hasura') 
main('mulx10','OpenGenus','cosmos',headers)
'''