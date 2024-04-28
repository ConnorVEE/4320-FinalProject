from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from Forms.OpeningForm import OpeningForm
from Forms.LoginForm import AdminLogin
from Forms.ReservationForm import Reservations

import sqlite3
from datetime import datetime

app = Flask(__name__)

### Database Functions ###

def get_db_connection(db_path='./Database/reservations.db'): #establish db connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Save new reservation data
def save_new_user(fname, seatRow, seatColumn, eTicketNumber):

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Get the current timestamp
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Insert a new row into the 'reservations' table
        cursor.execute("INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber, created) VALUES (?, ?, ?, ?, ?)",
                       (fname, seatRow, seatColumn, eTicketNumber, created))
        # Commit the transaction
        conn.commit()
    finally:
        conn.close()

# Authorize admin login. Make sure the user logging in is an admin
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

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
    return cost_matrix

def calculate_total_sales():
    seating_info = get_seating_info()
    cost_matrix = get_cost_matrix()
    total_sales = 0

    for seat in seating_info:
        row_index = int(seat['seat_row']) - 1
        col_index = int(seat['seat_column']) - 1
        seat_price = cost_matrix[row_index][col_index]
        total_sales += seat_price

    return total_sales


### Application Functions ###

# Create unique user key 
def keyCreator(name):
    keyWord = "INFOTC4320"
    meshed = ''

    # Determine the length of the longer string
    max_len = max(len(name.data), len(keyWord))
    
    # Iterate through both strings simultaneously
    for i in range(max_len):
        if i < len(name.data):
            meshed += name.data[i]
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

        # Save new user data to the database
        save_new_user(form.firstName.data, form.seatRow.data, form.seatColumn.data, userKey)

        # Refresh seating info after saving the new user data
        seating_info = get_seating_info()

        return render_template('reservations.html', form=form, seating_info=seating_info, userKey=userKey) 
    
    return render_template('reservations.html', form=form, seating_info = seating_info)

## Admin View Page
@app.route('/adminView', methods={'GET', 'POST'})
def adminView():
    ## Get seating info from db
    seating_info = get_seating_info()
    total_Sales = calculate_total_sales()

    return render_template("adminView.html", seating_info = seating_info, total_Sales = total_Sales)

if __name__ == '__main__':
    app.run(debug=True)