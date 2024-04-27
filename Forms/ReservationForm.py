from flask_wtf import FlaskForm
from wtforms.validators import NumberRange
from wtforms import (
    SubmitField,
    StringField,
    IntegerField
)

from wtforms.validators import DataRequired

class Reservations(FlaskForm):

    firstName = StringField("Enter your first name", [DataRequired(message="First name is required.")])
    
    lastName = StringField("Enter your last name", [DataRequired(message="Last name is required")])
    
    seatRow = IntegerField("Enter the row number (1-12)", [DataRequired(message="Seat row is required."), NumberRange(min=1, max=12, message="Row number must be an integer between 1-12")])
    
    seatColumn = IntegerField("Enter the column number (1-4)", [DataRequired(message="Seat column is required."), NumberRange(min=1, max=4, message="Column number must be an integer between 1-4")])
    
    submit = SubmitField("Confirm Reservation")
    
  
    
