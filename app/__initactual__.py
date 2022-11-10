# TEAM FERRARI: Abid Talukder, Craig Chen, Raven Tang
# SoftDev
# K19 -- SESSIONS
# 2022-11-05

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

DB_FILE="database.db"
file = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
db = file.cursor()

def add_user(username, email, password, phone):
    key = str(os.urandom(16))
    insert = f"insert into users values('{username}','{email}', '{password}', '{phone}', '{key}');"
    db.execute(insert)

@app.route("/") # At the root, we just return the homepage
def index():
    return render_template("signup.html")
    
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # create_table = "create table users(username text, email text, password text, phone text, id text);"
        # db.execute(create_table)
        add_user(request.form.get("username"),request.form.get("email"), request.form.get("password"),request.form.get("phone"))
    file.commit()
    db.execute("SELECT * FROM users;")
    print(db.fetchall())
    
    return render_template("home.html")

@app.route("/auth",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':   
        filter_cmd = f'SELECT * from users'
        # where username="{request.form.get("username")}" and password="{request.form.get("password")}"
        try:
            db.execute(filter_cmd)
            user = db.fetchall()
            print()
            # session["username"]= user[0]
            # session["email"]=user[1]
            # session["phone"]=user[3]
            # session["userid"] = user[4]
            return render_template("home.html")
        except:
            return render_template("login.html")
            
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
    
        
    
        
        


