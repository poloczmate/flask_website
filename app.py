#!/bin/python

import re
from flask import Flask, render_template, redirect, url_for, request
import base64
import hashlib
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 26000


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

def hash_password(password, salt=None): #function to hash the passwords
    if salt is None:
        salt = secrets.token_hex(16)    #get a random string in hex
    
    pw_hash = hashlib.pbkdf2_hmac(  #using hmac as hashing algorithm
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), ITERATIONS
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()    #encode it to base64
    return "{}${}".format(salt, b64_hash)  #return salt and password

def verify_password(password, password_hash, salt):
    compare_hash = hash_password(password, salt)    #hash the password with the function above
    return secrets.compare_digest(password_hash, compare_hash)  #true or false?