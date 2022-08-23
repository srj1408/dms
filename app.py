# from fileinput import filename
# from importlib.resources import contents
# from operator import contains
# from unittest import result
# from webbrowser import get
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import boto3

app = Flask(__name__)
app.secret_key = 'rahul-maurya'

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Rahul@123"

conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)

# @app.route('/',methods=['GET','POST'])
# def home():
    
#     if 'loggedin' in session:

#         return render_template('home.html',username=session['username'])
#     return redirect(url_for('login'))

# @app.route('/upload',methods=['post'])
# def upload():
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
#     if request.method == 'POST':
#         pdf = request.files['file']
#         if pdf:
#                 username=session['username']
#                 filename = "DOC" + datetime.now().strftime("%d%m%y%I%M%S") + ".pdf" #date_format
#                 pdf.save(filename)
#                 s3 = boto3.client("s3")
#                 s3.upload_file(  
#                     Filename = filename,
#                     Bucket = "ims2022",
#                     Key = filename,
#                 )
#                 cursor.execute("INSERT INTO upload (username, upload_files) VALUES (%s,%s)", (username,filename))
#                 conn.commit()
#                 cursor.close()
#                 msg = "Upload Done ! "
#         else:
#             msg = "Please select a file to upload! "
#         return render_template("home.html",msg =msg)
@app.route('/',methods=['GET','POST'])
def home():
    
        return render_template('login.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    if 'loggedin' in session:
        try:
            if request.method == 'POST':
                pdf = request.files['file']
                if pdf:
                        username=session['username']
                        filename = "DOC" + datetime.now().strftime("%d%m%y%I%M%S") + ".pdf" #date_format
                        pdf.save(filename)
                        s3 = boto3.client("s3")
                        s3.upload_file(  
                        Filename = filename,
                        Bucket = "ims2022",
                        Key = filename,
                    )
                        cursor.execute("INSERT INTO upload (username, upload_files) VALUES (%s,%s)", (username,filename))
                        conn.commit()
                        msg = "Upload Done ! "
                else:
                    msg = "Please select a file to upload! "
                return render_template("home.html",msg=msg)
        finally:
            cursor.close()
        return render_template("home.html",username=session['username'])
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET','POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account: 
            password_rs = account['password']
            _hashed_password = generate_password_hash(password_rs)
            print(_hashed_password)
            print(password)
            if check_password_hash(_hashed_password, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('upload'))
            else:
                flash('Incorrect username or password')
        else:
            flash('Incorrect username or password')

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)