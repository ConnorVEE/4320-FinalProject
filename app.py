from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from Forms.OpeningForm import OpeningForm
from Forms.LoginForm import AdminLogin

app = Flask(__name__)

import sqlite3

def get_db_connection(db_path='./Database/reservations.db'): #establish db connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def authorize_admin_login(username, password): #authenticate admin login
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admins WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result and result['password'] == password:
            return True
        return False
    finally:
        conn.close()

def add_reservation(): #add parameters, method to check if reserved spot is already taken, if not add passenger
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
    finally:
        conn.close()
                    
# Generate a secret key. This key will be used to help with security and authentication
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def start():
    form = OpeningForm()
    
    if form.validate_on_submit():
        action = form.action_type.data

        if action == "1":
            return redirect('/login')  # Redirect to the login page
        elif action == "2":
            return redirect('/reservations') # Redirect to the reservations page

    return render_template("start.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLogin()
    if form.validate_on_submit():
        username = form.admin_user.data
        password = form.admin_passwd.data
        if authorize_admin_login(username, password):
            return #add logic to add the chart and total sales upon successful login
        else:
            err = 'Incorrect username or password.'
            return render_template("login.html", form=form, err=err)
            
    return render_template("login.html", form=form)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    # Handle reservations page logic here
    return render_template("reservations.html")

if __name__ == '__main__':
    app.run(debug=True)