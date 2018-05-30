from src import app
from flask import Flask, render_template
# from flask import jsonify
from src.backend import *

@app.route("/")
def home():
    return "Hasura Hello World"

@app.route("/lang")
def index():
    return render_template("lang.html",langreport=[{'lang':'python','w1':100,'w2':4},{'lang':'python','w1':3,'w2':4}])
# Uncomment to add a new URL at /new

@app.route("/json")
def json_message():
    return jsonify(message="Hello World")
