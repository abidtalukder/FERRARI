# TEAM FERRARI: Abid Talukder, Craig Chen, Raven Tang
# SoftDev
# K19 -- SESSIONS
# 2022-11-05

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
username="ferrari"
password="ferrari"


'''
trioTASK:
~~~~~~~~~~~ BEFORE RUNNING THIS, ~~~~~~~~~~~~~~~~~~
...read for understanding all of the code below.
Some will work as written; other sections will not. 
TASK: Predict which...
Devise some simple tests you can run to "take apart this engine," as it were.
Execute your tests.
Process results.</html>
PROTIP: Insert your own in-line comments
 wherever they will help
  your future self and/or current teammates
   understand what is going on.
'''

@app.route("/") #, methods=['GET', 'POST'])
def disp_loginpage():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print("***DIAG: request.headers ***")
    print(request.headers)
    try:
      if session['username'] == username and session['password'] == password:
        return render_template("response.html", user=username,)
    except:
      return render_template( 'login.html' )


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    print("***DIAG: request obj ***")
    print(request)
    print("***DIAG: request.args ***")
    print(request.args)
    #print("***DIAG: request.args['username']  ***")
    #print(request.args['username'])
    print("***DIAG: request.headers ***")
    print(request.headers)
    # reqstr = str(request)
    # if reqstr.find("GET") != -1:
    #     reqstr = "GET"
    # else:
    #     reqstr = "POST"
    try:
      if session['username'] == username and session['password'] == password:
        return render_template("response.html", user=username,)
    except:
      None
    
    # return f'Welcome to the Interweb, {request.form["username"]} <br><br> Your Request Method: ' + reqstr + f'<br><br> We Hope You Love This Website <br><br> '  #response to a form submission
    if request.method == 'POST':
        
        if request.form.get('username') == username and request.form.get("password") == password:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
        
            return render_template("response.html", user=username,)
                      
        else:
          
            if username != request.form.get('username'):
                return '''
                <html>

# TEAM FERRARI: Abid Talukder, Craig Chen, Raven Tang
<br>
  # SoftDev
  <br>
  # K19 -- SESSIONS
  <br>
  # 2022-11-05
  <br>


  <head>
    <title>Login </title>
  </head>

  <body>
    <h1> Welcome to the Interwebs, Traveller.
      <br>
      Hello user. It seems you are not logged in. Please log in.
    </h1>
    
    <br>
    <br>
    <h3>Error: Incorrect Username</h3>
    <br>
    <br>

    <h3>
      Enter your credentials
    </h3>
    <form action = "/auth" method = "POST">
      <input type="text" value="Enter Username" name="username">
      <input type="text" value="Enter Password" name="password">
      <input type="submit" name="sub1">
    </form>
    <br>
  </body>

</html>
                
                '''
            if password != request.form.get('password'):
                return '''
                <html>
                # TEAM FERRARI: Abid Talukder, Craig Chen, Raven Tang
<br>
  # SoftDev
  <br>
  # K19 -- SESSIONS
  <br>
  # 2022-11-05
  <br>

  <head>
    <title>Login </title>
  </head>

  <body>
    <h1> Welcome to the Interwebs, Traveller.
      <br>
      Hello user. It seems you are not logged in. Please log in.
    </h1>
    
    <br>
    <br>
    <h3>Error: Incorrect Password</h3>
    <br>
    <br>

    <h3>
      Enter your credentials
    </h3>
    <form action = "/auth" method = "POST">
      <input type="text" value="Enter Username" name="username">
      <input type="text" value="Enter Password" name="password">
      <input type="submit" name="sub1">
    </form>
    <br>
  </body>

</html>
                
                '''
      
                
                  
# request.args["username"]
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return render_template("login.html")
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()