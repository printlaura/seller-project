from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash
from app.models.brand_manager import BrandManager


class BrandManagerSignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        brand_manager = BrandManager.query.filter_by(contact_email=email.data).first()
        if brand_manager:
            raise Error('This email is already in use. Please use a different one.')

    def hash_password(self):
        return generate_password_hash(self.password.data)


class BrandManagerLogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Email is required"), Email(message="Invalid email address")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')