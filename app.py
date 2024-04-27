from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from Forms.OpeningForm import OpeningForm
from Forms.LoginForm import AdminLogin
from Forms.ReservationForm import Reservations

import sqlite3

app = Flask(__name__)

### Database Functions ###

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

# retrieve seating info

def get_seating_info():
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        rows = cursor.fetchall()

        # Process the fetched data
        seating_info = []
        for row in rows:
            
            passengerID = row['id']
            passengerName = row['passengerName']
            seatRow = row['seatRow']
            seatColumn = row['seatColumn']
            eTicketNumber = row['eTicketNumber']
            created = row['created']

            seating_info.append({'id': passengerID, 'passenger_name': passengerName, 'seat_row': seatRow + 1, 'seat_column': seatColumn + 1, 'eTicketNumber': eTicketNumber, 'created': created})
        return seating_info
    finally:
        conn.close()


### Application Functions ###

# Create unique user key 
def keyCreator(name):
    keyWord = "INFOTC4320"
    meshed = ''

    # Determine the length of the longer string
    max_len = max(len(name), len(keyWord))
    
    # Iterate through both strings simultaneously
    for i in range(max_len):
        if i < len(name):
            meshed += name[i]
        if i < len(keyWord):
            meshed += keyWord[i]
    
    return meshed

                    
# Generate a secret key. This key will be used to help with security and authentication
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

## Opening form
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


## Admin Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLogin()

    if form.validate_on_submit():
        username = form.admin_user.data
        password = form.admin_passwd.data

        if authorize_admin_login(username, password):
            print("Success")
            return redirect('/adminView')
        else:
            err = 'Incorrect username or password, please try again'
            return render_template("login.html", form=form, err=err) 
            
    return render_template("login.html", form=form)


# Make a reservation page
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    ## Get seating info from db
    seating_info = get_seating_info()

    # Handle reservations page logic here
    form = Reservations()

    if form.validate_on_submit():
        userKey = keyCreator(form.firstName)
        ### We still need to get the timestamp ###

        #Push new data to the database
        #This can be done with a function being created in the ^^ Databases functions section


        seating_info = get_seating_info()
        return render_template('reservations.html', form=form, seating_info = seating_info, userKey=userKey) 
        # return "Reservation confirmed! Thank you."
    
    return render_template('reservations.html', form=form, seating_info = seating_info)


## Admin View Page
@app.route('/adminView', methods={'GET', 'POST'})
def adminView():
    ## Get seating info from db
    seating_info = get_seating_info()

    return render_template("adminView.html", seating_info = seating_info)

if __name__ == '__main__':
    app.run(debug=True)