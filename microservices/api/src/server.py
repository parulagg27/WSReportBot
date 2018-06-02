import os
import signal
import subprocess
from src import app
from flask import Flask, render_template
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from src.utils.backend import get_weekly_report, get_language_report_week
from src.utils.login import login

headers = login('mehul','mehul@hasura')
p = None
@app.route("/")
def home():
    return "Hello Parul :P"

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