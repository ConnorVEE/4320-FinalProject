from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from Forms.OpeningForm import OpeningForm

app = Flask(__name__)

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
            return redirect('/reservations')  # Redirect to the reservations page

    return render_template("start.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login page logic here
    return render_template("login.html")

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    # Handle reservations page logic here
    return render_template("reservations.html")

if __name__ == '__main__':
    app.run(debug=True)