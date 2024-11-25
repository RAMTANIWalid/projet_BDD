import random
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime


app = Flask(__name__)
# create route to login
@app.route("/login")
def login():
    return render_template("index.html")

# create route to register
@app.route("/register")
def register():
    return render_template("register.html")
# create route manager main page
@app.route("/manager")
def manager():
    composant = ["Mouse", "heyrizhfuiahh hfhehhzudhe hfuhehf zhfhzuur hzurghd hzyyhz hzhyhge","gohan.jpeg"]
    return render_template("profile.html", composants = [composant for i in range(10)])
if __name__ == '__main__':
    app.run()