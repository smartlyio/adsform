"""Form object declaration."""
from datetime import date
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    MultipleFileField,
    TextAreaField,
    URLField
)
from wtforms.fields import DateField
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired, Length, Regexp, url
import json


class AdForm(FlaskForm):
    with open('countries_cities.json') as fp:
        data = json.load(fp)
        keys = data.keys()
        cities = data.values()

        countries = list(data)
        
        country = SelectField("Which country?🌎 *", [DataRequired()], choices=countries)
        city = SelectMultipleField("Which City to target? (first select country) *",  [DataRequired()], choices=[], validate_choice=False)
        language = SelectField("Which language? *", [DataRequired()], choices=["AZ", "CS", "DA", "DE", "EL", "EN", "ET", "FI", "HE", "HR", "HU", "JA", "KA", "KK", "LT", "LV", "NO", "PL", "RU", "SK", "SL", "SR", "SV"])
        adtitle = StringField("Write the title of your ad: *", [Length(max=25, message="Ad title must be betwen 2 & 25 characters"), DataRequired()])
        adcopy = TextAreaField("Write the copy of the ad: *", [Length(max=125, message="Ad copy must be betwen 2 & 125 characters"), DataRequired()])
        calltoaction = SelectField("Select a call to action: *", [DataRequired()], choices=["SHOP_NOW", "LEARN_MORE", "DOWNLOAD", "BUY_NOW", "ORDER_NOW", "ADD_TO_CART", "SEE_MORE"])
        startdate = DateField("Start Date *",[DataRequired()], format='%Y-%m-%d', default=date.today())
        enddate = DateField("End Date *", [DataRequired()], format='%Y-%m-%d', default=date.today())
        creativetype = SelectField("What kind of creative is it? *", [DataRequired()], choices=["local", "local-restaurants", "localretail", "local-partnership", "incentive-wolt", "incentive-partnership", "localretail-WM"])
        creativeconcept = StringField("Name of the creative concept? *", [Regexp('^\w+$', message="Concept must contain only letters numbers or underscore"), Length(max=25, message="Concept must be betwen 2 & 25 characters"), DataRequired()])
        adname = StringField("Name of the ad? *",[Regexp('^\w+$', message="Ad name must contain only letters numbers or underscore"), Length(max=25, message="Ad name must be betwen 2 & 25 characters"), DataRequired()])
        objective = SelectField("Would you like to run this ad for New users / Existing Users  or both? *", [DataRequired()], choices=["New Users", "Existing Users", "Both"])
        weblink = StringField("Web Link", default="")
        mobilelink = StringField("Mobile Link", default="")
        attachments = MultipleFileField('Image/Video upload: (jpg, png, svg or mp4) *')
        submit = SubmitField("Submit")


