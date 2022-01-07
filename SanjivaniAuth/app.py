from flask import Flask, render_template, jsonify, json, request, session,  redirect, url_for
from flask_cors import CORS , cross_origin
from flask.helpers import flash
from flask.sessions import NullSession
from flaskext.mysql import MySQL
import pymysql
from pymysql.cursors import Cursor 
import sns_noti
import md5
from datetime import datetime
import threading
from shutil import copyfile


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'Harsh@1526'

mysql=MySQL()
#mysql_config....................................................................................................................................
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sanjivani'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)
#................................................................................................................................................
def sqlconnect():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    conn.autocommit(True)
    
    return cursor

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    msg=""
    
    cursor=sqlconnect()
    if request.method == 'POST' and 'phone' in request.form and 'password' in request.form:
         # Create variables for easy access
         phone = request.form['phone']
         password = request.form['password']
         # Check if account exists using MySQL
         enc_pwd=md5.str2has(password)
         cursor.execute('SELECT * FROM users WHERE phone = %s AND password = %s', (phone, enc_pwd))
         # Fetch one record and return result
         account = cursor.fetchone()
   
         # If account exists in accounts table in out database
         if account:
            # Create session data, we can access this data in other routes
             print("exist")
             session['phone'] = account['phone']
             session['username']=account['username']
             print(account['is_active'])
             print(account['last_login'])
             otp="1234"
             session['otp']=otp;
             
             msg="otp"
            
             
         else:
              msg = '101 Incorrect username/password!'
              return jsonify({'msg':msg})
    else:
        msg="Some error"
        return jsonify({'msg':msg})
    return jsonify({"msg":msg})

@app.route("/auth", methods=['POST'])
def auth():
    otp_front=request.form['otp']
    msg=""
    phone=session['phone']
    otp_back=session['otp'];
    print("guess what?")
    if(otp_front==otp_back):
         session['loggedin'] = True
         print("all ok")
         session.pop('otp',None)
         print(session['username'])
         msg="loggedin"
         cursor=sqlconnect()
         cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(1),session['username']))
         cursor.execute('SELECT * FROM users WHERE username = %s ', (session['username']))
         account = cursor.fetchone()
         session['id'] = account['id']
         session['name']=account['first_name']
         session['email']=account['email']
         session['is_active']=account['is_active']
         session['privellage']=account['privellage']
         print(account['is_active']);
         last_login=account['last_login']
         print(last_login)
         now=datetime.now()
         session['last_login']=now.strftime("%Y-%m-%d %H:%M:%S")
         print(session['last_login'])
         date_joined=account['date_joined']


       
         return jsonify({
         "msg":msg, 
         })
    else:
             # Account doesnt exist or username/password incorrect
        msg = 'Wrong OTP'
        return jsonify({'msg':msg})





    
@app.route("/logout", methods=['POST','GET']) 
def logout():
    if(request.method=='POST' and 'info' in request.form):

     if(request.form['info']=="logout"):
       
       cursor=sqlconnect()
       cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(0),session['username']))
       cursor.execute('UPDATE users SET last_login=%s WHERE users.username = %s',(session['last_login'],session['username']))

       session.pop('loggedin', None)
       session.pop('id', None)
       session.pop('username', None)
       session.pop('is_active',None)
       session.pop('email',None)
       session.pop('phone',None)
       return jsonify({"msg":"loggedout"})
     elif(request.form['info']=="timeout"):
       cursor=sqlconnect()
       cursor.execute('UPDATE users SET is_active = %s WHERE users.username = %s',(int(0),session['username']))
       cursor.execute('UPDATE users SET last_login=%s WHERE users.username = %s',(session['last_login'],session['username']))
       return jsonify({"status":"offline"})
         
     else:
        return jsonify({"msg","some error"})
    else:
        return redirect("/dashboard")


if __name__ == "__main__":
    
    app.run(host='127.0.0.1', port=40, debug=True)