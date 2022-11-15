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
dblogs = ""


def get_random_string():
    length = 16
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str    

def create_genre_string(login_answer):
    if("adventure" in login_answer.lower()):
        return "1,0,0,0,0"
    if("humor" in login_answer.lower()):
        return "0,1,0,0,0"
    if("network" in login_answer.lower()):
        return "0,0,1,0,0"

    if("scary" in login_answer.lower()):
        return "0,0,0,1,0"

    return "0,0,0,0,1"


def update_genre_string(genre, genre_str):
     genre_split = genre_str.split(",")
     if("Adventure".lower() in genre.lower()):
         genre_split[0] = int(genre_split[0]) + 1
     
     elif("humor".lower() in genre.lower() ):
         genre_split[1] = int(genre_split[1]) + 1
     
     elif("Network".lower() in genre.lower()):
         genre_split[2] = int(genre_split[2]) + 1
     
     elif("Scary".lower() in genre.lower()):
         genre_split[3] = int(genre_split[3]) + 1
     
     else:
         genre_split[4] = int(genre_split[4]) + 1
     
     return str(genre_split[0]) + "," + str(genre_split[1]) + "," + str(genre_split[2]) + "," + str(genre_split[3]) + "," + str(genre_split[4])

    
def parse_genre_string(genre_str):
     genre_split = genre_str.split(",")
     # adventure (0), humor (1), network (2), scary (3), science (4)
     curr_max = 0
     for i in range(5):
         genre_split[i] = int(genre_split[i])
         if(genre_split[i] > genre_split[curr_max]):
             curr_max = i
         
     
     if curr_max == 0:
        return "Adventure"
     elif curr_max == 1:
        return "Humor"
     elif curr_max == 2:
        return "Network"
     elif curr_max == 3:
        return "Scary"
     else:
        return "Science"

def get_blogs():
    # most_liked = parse_genre_string(session["genres"])
    # filter_command = f"SELECT * from blogs where genre like '{most_liked}'"
    # db.execute(filter_command)
    db.execute(f"SELECT * from blogs where userid not like '{session['userid']}'")
    dblogs = db.fetchall()
    return dblogs

DB_FILE="database.db"
file = sqlite3.connect(DB_FILE,check_same_thread=False) #open if file exists, otherwise create
db = file.cursor()

def add_user(username, email, password, phone):
    key = str(os.urandom(16))
    insert = f"insert into users values('{username}','{email}', '{password}', '{phone}', '{key}');"
    db.execute(insert)
    
def update_articles():
    filter_articles = f"Select * from blogs where userid like '{session['userid']}'"
    db.execute(filter_articles)
    blog_list = db.fetchall()
    session["blog_list"] = blog_list
    return blog_list

@app.route("/",methods=['GET', 'POST']) # At the root, we just return the homepage
def index():
    try:
        session['username']
        return render_template("home.html", user=session["username"], blogs = get_blogs())
    except:
        return render_template("index.html")
        
@app.route("/profile",methods=['GET', 'POST'])
def profile():
    return render_template("profile.html", user=session['username'], blogs=update_articles())
    
@app.route("/signupPage",methods=['GET', 'POST'])
def signupPage():
    return render_template("signup.html")
    
@app.route("/loginPage",methods=['GET', 'POST'])
def loginPage():
    return render_template("login.html")
    
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # create_table = "create table users(username text, email text, password text, phone text, id text);"
        # db.execute(create_table)
        
        key = get_random_string()
        
        has_key = False
        
        # while True:
        #     try:
        #         db.execute(f"select * from users where id like '{key}';")
        #         key = get_random_string()
        #     except:
        #         break
            
        
        username = str(request.form.get('username'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        phone = str(request.form.get('phone'))
        g = create_genre_string(str(request.form.get('genres')))
        
        command = f"insert into users values('{username}','{email}','{password}','{phone}','{key}', '{g}');"
        db.execute(command)
        
    file.commit()
    
    # Saving cookie information
    session["username"]= username
    session["email"]=email
    session["phone"]=password
    session["userid"] = phone
    
    
    # db.execute("SELECT * FROM users;")
    # print(db.fetchall())
    
    return render_template("home.html", user=session["username"], blogs = get_blogs())

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
            session["genres"] = user[0][5]
           
            
            update_articles()
            
            # html_blog_display = []
            # for blog in blog_list:
            #     a = f'''
            #     <form action = "/edit" method = "POST">
            #         <input type="hidden" name="blogId" value="{blog[1]}">
            #         <input type="submit" value="Edit Blog" name="xyz">
            #     </form>
            #     '''
            #     html_blog_display.append(a)
        
            return render_template("home.html", user=session["username"], blogs = get_blogs())
        except:
            return render_template('login.html')
            
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('email', None)
    session.pop('phone', None)
    session.pop('userid', None)
    session.pop("genres", None)
    return render_template("index.html")

# COMPLETING AUTHENTICATION METHODS
 
# STARTING ARTICLE CREATION METHODS
@app.route('/createBlogs', methods=['GET', 'POST'])
def updateBlogs():
    return render_template("createBlog.html")
    
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
    update_articles()
        
    return render_template("profile.html", user=session['username'], blogs=session['blog_list'])
    
@app.route('/editBlog', methods=['GET', 'POST'])
def editBlog():
    if request.method == 'POST':
        blogId = request.form.get("blogId")
        filter_articles = f"Select * from blogs where articleid like '{blogId}'"
        db.execute(filter_articles)
        blog_list = db.fetchall()[0]
        
        return render_template('editBlog.html', blog=blog_list)

@app.route('/saveEdit', methods=['GET', 'POST'])
def saveEdit():
    if request.method == 'POST':
        genres=request.form.get('genre')
        title = request.form.get('title')
        content = request.form.get('content')
        blogid = request.form.get('blogId')
        creation_time = str(datetime.datetime.now())
        
        insert_blogs = f"  blogs SET title='{title}', content='{content}' WHERE articleid LIKE '{blogid}';"
        db.execute("UPDATE blogs SET title=?, content=? WHERE articleid LIKE ?", (title,content,blogid))
    
    file.commit()
        
    return render_template("profile.html", user=session['username'], blogs=update_articles())
        
@app.route('/deleteEntry', methods=['GET', 'POST'])      
def deleteEntry():
    try:
        command = f"DELETE FROM blogs where articleid LIKE '{request.form.get('blogId')}'"
        db.execute(command)
        file.commit()
    except: 
        None
    return render_template("profile.html", user=session['username'], blogs=update_articles())
    
    
### RECOMMENDATIONS ###
@app.route('/likeGenre', methods=['GET', 'POST'])
def likeGenre():
    
    return render_template("404.html")
    
@app.route('/displayBlogs', methods=['GET', 'POST'])
def displayBlogs():
    get_blogs()
    return render_template("home.html", user=session["username"], blogs = dblogs)
    
    
    
    
    
            
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
    
        
    
        
        




'''
0 - adventure
1 - humor 
2 - network
3 - scary
4 - science
'''
