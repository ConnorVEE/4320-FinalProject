from flask import Flask
from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)