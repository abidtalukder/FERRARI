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
import datetime
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(16)


def get_random_string():
    length = 16
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str

DB_FILE="database.db"
file = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
db = file.cursor()

def add_user(username, email, password, phone):
    key = str(os.urandom(16))
    insert = f"insert into users values('{username}','{email}', '{password}', '{phone}', '{key}');"
    db.execute(insert)

@app.route("/") # At the root, we just return the homepage
def index():
    return render_template("login.html")
    
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # create_table = "create table users(username text, email text, password text, phone text, id text);"
        # db.execute(create_table)
        
        key = get_random_string()
        username = str(request.form.get('username'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        phone = str(request.form.get('phone'))
        
        command = f"insert into users values('{username}','{email}','{password}','{phone}','{key}');"
        db.execute(command)
        
    file.commit()
    
    # Saving cookie information
    session["username"]= username
    session["email"]=email
    session["phone"]=password
    session["userid"] = phone
    
    
    # db.execute("SELECT * FROM users;")
    # print(db.fetchall())
    
    return render_template("home.html")

@app.route("/auth",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  
        # Filters if username and password matches
        filter_cmd = f"SELECT * from users where username LIKE '{request.form.get('username')}' and password LIKE '{request.form.get('password')}';"
        
        try:
            db.execute(filter_cmd)
            user = db.fetchall()
            #print(user)
            
            # Saves to cookie
            session["username"]= user[0][0]
            session["email"]=user[0][1]
            session["phone"]=user[0][3]
            session["userid"] = user[0][4]
        
            return render_template("profile.html", user=session['username'])
        except:
            return render_template('login.html')
            
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('email', None)
    session.pop('phone', None)
    session.pop('userid', None)
    return render_template("login.html")

# COMPLETING AUTHENTICATION METHODS
 
# STARTING ARTICLE CREATION METHODS
@app.route('/updateBlogs', methods=['GET', 'POST'])
def updateBlogs():
    return render_template("edit.html")
    
@app.route('/saveBlog',methods=['GET', 'POST'])
def saveBlog():
    if request.method == 'POST':
        articleid = get_random_string()
        
        genres=request.form.get('genre')
        title = request.form.get('title')
        content = request.form.get('content')
        creation_time = str(datetime.datetime.now())
        
        insert_blogs = f"insert into blogs values('{session['userid']}','{articleid}','{genres}','{title}','{content}','{creation_time}','{creation_time}');"
        db.execute(insert_blogs)
    
    file.commit()
        
    return render_template("profile.html")
    
       
    
    
            
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
    
        
    
        
        


