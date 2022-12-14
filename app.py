#!/bin/python
import re
from flask import Flask, render_template, redirect, url_for, request, flash
import base64
import hashlib
import secrets
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    username = 'root',
    password = 'qwerasdf00',
    database = 'flask_website'
)

cursor = mydb.cursor()

register_sql = "insert into Users (username, salt, password) values (%s, %s, %s);"
verify_sql = "select PASSWORD, SALT from Users where USERNAME =%s;"
ITERATIONS = 26000

def hash_password(password, salt=None): #function to hash the passwords
    if salt is None:
        salt = secrets.token_hex(16)    #get a random string in hex
    
    pw_hash = hashlib.pbkdf2_hmac(  #using hmac as hashing algorithm
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), ITERATIONS
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()    #encode it to base64
    return "{}${}".format(salt, b64_hash)  #return salt and password

def verify_password(password, password_hash, salt):
    compare_salt, compare_hash = hash_password(password,salt).split('$', 1)    #hash the password with the function above
    return secrets.compare_digest(password_hash, compare_hash)  #true or false?


app = Flask(__name__)

@app.route("/home")
def index():
	return render_template("home.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        if request.form["username"] != "" and request.form["password"] != "":
            salt, password = hash_password(request.form["password"]).split('$',1)
            tmp = (request.form["username"], salt, password)
            cursor.execute(register_sql,tmp)
            mydb.commit()
        else:
            print("error")
    return render_template("registration.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        try:
            tmp = (request.form["username"],)
            cursor.execute(verify_sql,tmp)
            results = cursor.fetchall()
            if verify_password(request.form["password"], results[0][0], results[0][1]):
                return redirect("home")
            else:
                print("Invalid credentials. Please try again.")
        except:
            print("Invalid credentials. Please try again.")
            return render_template("login.html")
    return render_template("login.html")

app.run(host="0.0.0.0", port = 5001)