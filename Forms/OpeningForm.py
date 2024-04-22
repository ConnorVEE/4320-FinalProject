from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    SelectField,
    SubmitField,
)

from wtforms.validators import URL, DataRequired, Email, EqualTo, Length

class OpeningForm(FlaskForm):
    
    action_type = SelectField("Where would you like to go?", [DataRequired()],
        choices=[
            ("1", "Admin Login"),
            ("2", "Reservations"),
        ], 
    )

    submit = SubmitField("Submit")
