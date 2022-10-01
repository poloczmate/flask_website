#!/bin/python

import re
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

@app.route("/home")
def index():
	return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    #work to do
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid credentials. Please try again."
        else:
            return redirect("home")
    return render_template("login.html")

app.run(host="0.0.0.0", port = 5001)