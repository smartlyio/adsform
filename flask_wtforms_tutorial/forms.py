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
from flask_wtf.file import FileField, FileRequired
from wtforms import MultipleFileField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import json

class AdForm(FlaskForm):
    with open('countries_cities.json') as fp: # todo migrate to a db once app is launched
        data = json.load(fp)
        keys = data.keys()
        countries = list(data)
        
        country = SelectField("Which country? 🌎", [DataRequired()], choices=countries)
        city = SelectField("Which City to target? (first select country)", [DataRequired()], validate_choice=False)
        language = SelectField("Which language?", [DataRequired()], choices=["AZ", "CS", "DA", "DE", "EL", "EN", "ET", "FI", "HE", "HR", "HU", "JA", "KA", "KK", "LT", "LV", "NO", "PL", "RU", "SK", "SL", "SR", "SV"])
        adtitle = StringField("Write the title of your ad:", [DataRequired()])
        adcopy = StringField("Write the copy of the ad:", [DataRequired()])
        calltoaction = SelectField("Select a call to action:", [DataRequired()], choices=["SHOP_NOW", "LEARN_MORE", "DOWNLOAD", "BUY_NOW", "ORDER_NOW", "ADD_TO_CART", "SEE_MORE"])
        startdate = DateField("Start Date (leave as-is for empty)", format='%Y-%m-%d', default=date(1111,11,11))
        enddate = DateField("End Date (leave as-is for empty)", format='%Y-%m-%d', default=date(1111,11,11))
        creativetype = SelectField("What kind of creative is it?", [DataRequired()], choices=["local", "local-restaurants", "localretail", "local-partnership", "incentive-wolt", "incentive-partnership"])
        creativeconcept = StringField("Name of the creative concept?", [DataRequired()])
        adname = StringField("Name of the ad?", [DataRequired()])
        objective = SelectField("Would you like to run this ad in UA or R&F?", [DataRequired()], choices=["UA", "Reach & Frequency", "Both"])
        attachment = FileField('Image/Video upload: (jpg, png, svg or mp4)')
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
