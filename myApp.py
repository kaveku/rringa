from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
import re

app = Flask(__name__)
app.secret_key = '584tyh34'


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "fruits"

    def mysqlconnect(self):
        # To connect MySQL database
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            db="fruits"
        )
        return conn

@app.route('/product')
def product():
    def db_query():
        db = Database()
        conn = db.mysqlconnect()
        cur = conn.cursor()

        # Select query
        cur.execute("select * from banana")
        output = cur.fetchall()

        # for i in output:
        # print(i)

        # To close the connection
        conn.close()
        return output

    res = db_query()

    return render_template("product.html", result=res)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Connecting to database
        # Select query
        def mydb_query():
            db = Database()
            conn = db.mysqlconnect()
            cur = conn.cursor()

            # Select query
            cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            output = cur.fetchone()

            # for i in output:
            # print(i)

            # To close the connection
            conn.close()
            return output

        account = mydb_query()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

        # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page using both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    db = Database()
    conn = db.mysqlconnect()
    cur = conn.cursor()

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Select query
        cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cur.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account does not exist and the form data is valid, now insert new account into accounts table
            cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()
            conn.close()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))