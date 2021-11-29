"""Form object declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import json

class AdForm(FlaskForm):
    """Ad Creation form."""
    
    name = StringField("Name", [DataRequired()])
    # form_name = HiddenField('Form Name')
    state = SelectField('State:', validators=[DataRequired()], id='select_state')
    county = SelectField('County:', validators=[DataRequired()], id='select_county')
    submit = SubmitField('Select County!')

class ContactForm(FlaskForm):
    with open('countries_cities.json') as fp: # todo migrate to a db once app is launched
        data = json.load(fp)
        countries = list(data.keys())
        cities = list(data.values())
        # countries.sort()
        # cities.sort()

    """Contact form."""
    country = SelectField("country", [DataRequired()], choices=[countries])
    city = SelectField("city", [DataRequired()], choices=[cities])
    name = StringField("Name", [DataRequired()])
    email = StringField(
        "Email",
        [Email(message="Not a valid email address."), DataRequired()]
    )
    body = TextAreaField(
        "Message",
        [DataRequired(), Length(min=4, message="Your message is too short.")]
    )
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    """Sign up for a user account."""

    email = StringField(
        "Email",
        [Email(message="Not a valid email address."), DataRequired()]
    )
    password = PasswordField(
        "Password",
        [DataRequired(message="Please enter a password.")],
    )
    confirmPassword = PasswordField(
        "Repeat Password",
        [EqualTo(password, message="Passwords must match.")]
    )
    title = SelectField(
        "Title",
        [DataRequired()],
        choices=[
            ("Farmer", "farmer"),
            ("Corrupt Politician", "politician"),
            ("No-nonsense City Cop", "cop"),
            ("Professional Rocket League Player", "rocket"),
            ("Lonely Guy At A Diner", "lonely"),
            ("Pokemon Trainer", "pokemon"),
        ],
    )
    website = StringField("Website", validators=[URL()])
    birthday = DateField("Your Birthday")
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")
