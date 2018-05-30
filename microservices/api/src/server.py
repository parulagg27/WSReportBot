from src import app
from flask import Flask, render_template
from flask import jsonify

@app.route("/")
def home():
    return "Hello Parul :P"

@app.route("/start")
def start():
    import subprocess
    subprocess.Popen(["python","src/utils/clock.py"])
    return "Hello Parul :P"

@app.route("/report")
def report():
    user_report = [{'handle':'mulx10',
                    'avatar_url':'https://avatars2.githubusercontent.com/u/23444642?v=4',
                    'name':'Mehul Kumar Nirala',
                    'details':'no need'},
                    {'handle':'parulagg27',
                    'avatar_url':'https://avatars1.githubusercontent.com/u/29358390?s=460&v=4',
                    'name':'Parul Aggarwal',
                    'details':'Learn. Improve. Evolve. Repeat'}]
    return render_template("cards.html",user_report=user_report, date="30 May, 2018")

@app.route("/lang")
def index():
    langreport = [{'lang':'python','w1':100,'w2':4},{'lang':'python','w1':3,'w2':4}]
    return render_template("lang.html",langreport=langreport)
# Uncomment to add a new URL at /new

@app.route("/json")
def json_message():
    return jsonify(message="Hello World")
