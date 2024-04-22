from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField, 
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from datetime import date
from wtforms.fields import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length


class OpeningForm(FlaskForm):
    
    action_type = SelectField("Where would you like to go?", [DataRequired()],
        choices=[
            ("1", "Admin Login"),
            ("2", "Reservations"),
        ], 
    )