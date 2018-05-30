from src import api
from flask import Flask, render_template
from flask import jsonify

@api.route("/")
def home():
    return "Hello Parul :P"

@api.route("/lang")
def index():
    return render_template("lang.html",langreport=[{'lang':'python','w1':100,'w2':4},{'lang':'python','w1':3,'w2':4}])
# Uncomment to add a new URL at /new

@api.route("/json")
def json_message():
    return jsonify(message="Hello World")
