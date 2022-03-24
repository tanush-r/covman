# Store this code in 'app.py' file
  
from curses.ascii import isalpha
from pydoc import render_doc
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import base64
  
  
app = Flask(__name__)
  
  
app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tan'
app.config['MYSQL_PASSWORD'] = '4757'
app.config['MYSQL_DB'] = 'covmanager'
  
mysql = MySQL(app)
  

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/student_login', methods =['GET', 'POST'])
def student_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            # return render_template('student_homepage.html', username = username)
            return redirect(url_for('student_homepage', username = username))
        else:
            msg = 'Incorrect username / password !'
    return render_template('student_login.html',msg=msg)

@app.route('/teacher_login', methods =['GET', 'POST'])
def teacher_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher_accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('teacher_homepage',username=username))
        else:
            msg = 'Incorrect username / password !'
    return render_template('teacher_login.html',msg=msg)

@app.route('/student_register', methods =['GET', 'POST'])
def student_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'usn' in request.form:
        username = request.form['username']
        usn = request.form['usn']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not usn:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO student_accounts(usn,username,password,email) VALUES (% s, % s, % s, % s)', (usn, username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('student_register.html', msg = msg)

@app.route('/teacher_register', methods =['GET', 'POST'])
def teacher_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'teacher_id' in request.form:
        username = request.form['username']
        teacher_id = request.form['teacher_id']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher_accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not teacher_id:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO teacher_accounts(teacher_id,username,password,email) VALUES (% s, % s, % s, % s)', (teacher_id, username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('teacher_register.html', msg = msg)

@app.route('/student_details', methods =['GET', 'POST'])
def student_details():
    msg = ''
    username = request.args.get("username")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT usn FROM student_accounts WHERE username = % s', (username, ))
    account = cursor.fetchone()
    usn = account['usn']
    print(account)
    if request.method == 'POST' and 'fullname' in request.form and 'semester' in request.form and 'section' in request.form and 'phone_no' in request.form and 'address' in request.form:
        fullname = request.form['fullname']
        semester = request.form['semester']
        section = request.form['section']
        phone_no = request.form['phone_no']
        address = request.form['address']
        print(request.files)
        # cert = request.files['cert'].read()
        
        semester = int(semester)
        print(type(semester))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_details WHERE usn = % s', (usn, ))
        account = cursor.fetchone()
        if account:
            msg = 'Details already filled !'
        elif semester < 1 or semester > 8:
            msg = 'Invalid semester !'
        elif not isalpha(section) :
            msg = 'Wrong section'
        elif len(phone_no) != 10:
            msg = 'Wrong Phone no'
        elif not fullname or not semester or not section or not phone_no or not address:
            msg = 'Please fill out the form !'
        else:
            # cert_blob = base64.b64encode(cert)
            # phone_no = int(phone_no)
            cursor.execute('INSERT INTO student_details(usn,name,semester,section,ph_no,address,cert) VALUES (% s, % s, % s, % s, % s, % s, % s)', (usn,fullname,semester,section,phone_no,address, "101"))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('student_cert.html',username=username)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('student_details.html', usn=usn, msg = msg,username = username)

@app.route('/student_cert', methods =['GET', 'POST'])
def student_cert():
    msg = ''
    username = request.args.get("username")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT usn FROM student_accounts WHERE username = % s', (username, ))
    account = cursor.fetchone()
    usn = account['usn']
    
    if request.method == 'POST' and 'cert' in request.files:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM student_details WHERE cert != % s && usn =', ("101", ))
        # account = cursor.fetchone()
        # if account:
        #     msg = 'File already uploaded
        # else :
        cert = request.files['cert'].read()
        cert_blob = base64.b64encode(cert)
        cursor.execute('UPDATE student_details SET cert = % s WHERE usn = % s' , (cert_blob,usn, ))
        mysql.connection.commit()
        # msg = 'You have successfully registered !'
        # return render_template('student_cert.html',msg = msg)
        return render_template('student_homepage.html',username = username)

    return render_template('student_details.html', msg = msg)

@app.route('/student_homepage')
def student_homepage():
    username = request.args.get("username")
    return render_template("student_homepage.html",username=username)

@app.route('/teacher_homepage', methods =['GET', 'POST'])
def teacher_homepage():
    username = request.args.get("username")
    msg = ""
    student = ""
    if request.method == 'POST' and 'usn' in request.form:
        usn = request.form['usn']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_details WHERE usn = % s', (usn, ))
        student = cursor.fetchone()
        print(student)
        if not student:
            msg = 'USN not found'
        else :
            return render_template('teacher_homepage.html',username = username,student=student)
            
            
    return render_template("teacher_homepage.html",username=username,student=student)

@app.route('/pdf_view')
def pdf_view():
    usn = request.args.get("usn")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT cert FROM student_details WHERE usn = % s', (usn, ))
    cert = cursor.fetchone()
    pdf_data = cert["cert"]
    data = base64.b64decode(pdf_data)
    response = make_response(data) 
    cd = f"attachment; filename=Main.pdf" 
    response.headers['Content-Disposition'] = cd 
    response.mimetype='application/pdf' 
    print("Reache")
    return response

@app.route('/temperature')
def temperature():
    msg = ""
    return render_template("temperature.html",msg=msg)

if __name__ == '__main__':
    app.run(debug=True)