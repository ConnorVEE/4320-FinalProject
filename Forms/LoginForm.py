from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField
)

from wtforms.validators import DataRequired

class AdminLogin(FlaskForm):

    admin_user = StringField("Username", [DataRequired(message="Username is required.")])
    
    admin_passwd = StringField("Password", [DataRequired(message="Password is required")])
    
    sumbit = SubmitField("Login")