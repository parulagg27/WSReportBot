from src import app
from flask import Flask, render_template
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from src.utils.backend import get_weekly_report
from src.utils.login import login

@app.route("/")
def home():
    return "Hello Parul :P"

@app.route("/start")
def start():
    import subprocess
    subprocess.Popen(["python","src/utils/clock.py"])
    return "Hello Parul :P"

@app.route("/report/<org_name>")
def report(org_name):
    print(org_name)
    headers = login('mehul','mehul@hasura')
    # org_name = 'KRSSG'
    T = datetime(month=5,day=8,year=2018)+timedelta(days=7)
    user_report, date = get_weekly_report(org_name = org_name,headers = headers,day = T)
    # user_report = [{
    #                     'handle':'mulx10',
    #                     'avatar_url':'https://avatars2.githubusercontent.com/u/23444642?v=4',
    #                     'name':'Mehul Kumar Nirala',
    #                     'lines_added':'1000+',
    #                     'lines_removed':'10+',
    #                     'no_of_commits':'38',
    #                     'pr_open':'3',
    #                     'pr_closed':'3'
    #                 },
    #                 {
    #                     'handle':'parulagg27',
    #                     'avatar_url':'https://avatars1.githubusercontent.com/u/29358390?s=460&v=4',
    #                     'name':'Parul Aggarwal',
    #                     'lines_added':'1000+',
    #                     'lines_removed':'10+',
    #                     'no_of_commits':'38',
    #                     'pr_open':'3',
    #                     'pr_closed':'3'
    #                 }]
    # date = "30 May, 2018"
    return render_template("cards.html",user_report=user_report, date=date)

@app.route("/lang")
def index():
    langreport = [{'lang':'python','w1':100,'w2':4},{'lang':'python','w1':3,'w2':4}]
    return render_template("lang.html",langreport=langreport)
# Uncomment to add a new URL at /new

@app.route("/json")
def json_message():
    return jsonify(message="Hello World")
