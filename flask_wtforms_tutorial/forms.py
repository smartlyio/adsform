"""Form object declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import json

class ContactForm(FlaskForm):
    with open('countries_cities.json') as fp: # todo migrate to a db once app is launched
        data = json.load(fp)
        keys = data.keys()
        countries = list(data)
        
        country = SelectField("Country", [DataRequired()], choices=countries)
        city = SelectField("City", [DataRequired()], choices=[])
        language = SelectField("Language", [DataRequired()], choices=["AZ", "CS", "DA", "DE", "EL", "EN", "ET", "FI", "HE", "HR", "HU", "JA", "KA", "KK", "LT", "LV", "NO", "PL", "RU", "SK", "SL", "SR", "SV"])
        adtitle = StringField("AdTitle", [DataRequired()])
        adcopy = StringField("AdCopy", [DataRequired()])
        calltoaction = SelectField("CallToAction", [DataRequired()], choices=["SHOP_NOW", "LEARN_MORE", "DOWNLOAD", "BUY_NOW", "ORDER_NOW", "ADD_TO_CART", "SEE_MORE"])
        startdate = DateField("Start Date", [DataRequired()], format='%Y-%m-%d')
        enddate = DateField("End Date", [DataRequired()], format='%Y-%m-%d')
        creativetype = SelectField("CreativeType", [DataRequired()], choices=["local", "local-restaurants", "localretail", "local-partnership", "incentive-wolt", "incentive-partnership"])
        creativeconcept = StringField("CreativeConcept", [DataRequired()])
        adname = StringField("AdName", [DataRequired()])
        objective = SelectField("Objective", [DataRequired()], choices=["UA", "Reach & Frequency", "Both"])
        attachment = FileField('attachment' , validators=[FileRequired()])
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
