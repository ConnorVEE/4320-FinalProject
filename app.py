from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

app = Flask(__name__)

# Generate a secret key. This key will be used to help with security and authentication
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)