"""Form object declaration."""
from datetime import date
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileRequired
from wtforms import MultipleFileField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import json

class AdForm(FlaskForm):
    with open('countries_cities.json') as fp: # todo migrate to a db once app is launched
        data = json.load(fp)
        keys = data.keys()
        countries = list(data)
        
        country = SelectField("Country", [DataRequired()], choices=countries)
        city = SelectField("City", [DataRequired()], validate_choice=False)
        language = SelectField("Language", [DataRequired()], choices=["AZ", "CS", "DA", "DE", "EL", "EN", "ET", "FI", "HE", "HR", "HU", "JA", "KA", "KK", "LT", "LV", "NO", "PL", "RU", "SK", "SL", "SR", "SV"])
        adtitle = StringField("Ad title", [DataRequired()])
        adcopy = StringField("Ad copy", [DataRequired()])
        calltoaction = SelectField("Call to action", [DataRequired()], choices=["SHOP_NOW", "LEARN_MORE", "DOWNLOAD", "BUY_NOW", "ORDER_NOW", "ADD_TO_CART", "SEE_MORE"])
        startdate = DateField("Start Date", format='%Y-%m-%d', default=date(1111,11,11))
        enddate = DateField("End Date", format='%Y-%m-%d', default=date(1111,11,11))
        creativetype = SelectField("Creative type", [DataRequired()], choices=["local", "local-restaurants", "localretail", "local-partnership", "incentive-wolt", "incentive-partnership"])
        creativeconcept = StringField("Creative concept", [DataRequired()])
        adname = StringField("Ad Name", [DataRequired()])
        objective = SelectField("Objective", [DataRequired()], choices=["UA", "Reach & Frequency", "Both"])
        attachment = MultipleFileField('Creative upload' , validators=[FileRequired()])
        # attachment = FileField('Creative upload' , validators=[FileRequired()])
        #  FileAllowed(['jpg', 'png', 'mp4', 'gif'], 'Images or videos only!')]
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
