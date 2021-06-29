
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange



class UserForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(message = 'Name is required'), Length(min=1, max=120,message = 'Name must be between 1 and 120 characters')])
    age = FloatField('Age (in years)',
                        validators=[DataRequired(message = 'Age is required'),NumberRange(min=0, max=100,message = "Maximum age limit is 100")])

    fare = FloatField('Fare (in £)',
                        validators=[DataRequired(message = 'Fare is required'),NumberRange(min=5, max=512,message = "Fare is between £5 and £512")])
    submit = SubmitField('get on titanic')
