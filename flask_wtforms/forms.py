"""Form object declaration."""
from datetime import date
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    MultipleFileField
)
from wtforms.fields import DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import json

class AdForm(FlaskForm):
    with open('countries_cities.json') as fp:
        data = json.load(fp)
        keys = data.keys()
        cities = data.values()

        countries = list(data)
        
        country = SelectField("Which country? 🌎", [DataRequired()], choices=countries)
        city = SelectMultipleField("Which City to target? (first select country)", [DataRequired()], choices=[], validate_choice=False)
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


