"""Routing."""
from flask import current_app as app
from flask import request, redirect, render_template, url_for, jsonify
from .forms import AdForm, SignupForm
from .googleint import *
from datetime import datetime
from werkzeug.utils import secure_filename
import json


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        template="home-template",
        title="Ad Creator Form App"
    )

@app.route('/getcities', methods=["GET", "POST"])
def pick_county():
    try:
        countryId = request.args.get('countryId', "DEU", type=str)
        if countryId != '':
            with open('countries_cities.json') as fp: # todo migrate to a db once app is launched
                data = json.load(fp)
            return jsonify(result=data[countryId])
        else:
            return jsonify(result=[''])
    except Exception as e:
        return str(e)

@app.route("/createad", methods=["GET", "POST"])
def createad():
    """Create ads"""
    form = AdForm(request.form)
    print(form['attachment'].data)
    if form.validate_on_submit():
        att = request.files.getlist(form.attachment.name)
        filelink = ''
        if att:
            for picture_upload in att:
                picture_contents = picture_upload.stream.read()
                print(type(picture_contents))
                # upload file to google drive
                file_link = write_into_drive(picture_contents, att[0]) # form.file.data.filename
                print(file_link)
        else:
            return render_template(
            "adcreation.jinja2",
            form=form,
            template="form-template",
            title="Create Ad Form"
        )
        print(file_link)
        #if  date == (Date(1111,11,11)) add empty
        ad_data = [
            # datetime.now().strftime("%m/%d/%Y"),
            form['language'].data,
            # mimetype (image or video)
            form['adcopy'].data,
            form['adtitle'].data,
            form['calltoaction'].data,
            # form['startdate'].data,
            # form['enddate'].data,
            form['creativetype'].data,
            form['creativeconcept'].data,
            form['adname'].data,
            # "x", # mediasize
            # "y", # video length
            file_link,
            form['country'].data,
            form['city'].data,
            form['objective'].data,
            # "coord", # coordinates
            # "live", # live
            # "fb", # fb page
            # "instagram"# instagram account
        ]
        write_status = write_into_sheet(ad_data)
        if write_status == 'ok':
            return redirect(url_for("success"))
        else:
            return render_template(
            "adcreation.jinja2",
            form=form,
            template="form-template",
            title="Create Ad Form"
        )

    return render_template(
        "adcreation.jinja2",
        form=form,
        template="form-template",
        title="Create Ad Form"
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "signup.jinja2",
        form=form,
        template="form-template",
        title="Signup Form"
    )

@app.route("/comingsoon", methods=["GET", "POST"])
def comingsoon():
    """Coming soon page."""
    return render_template(
        "comingsoon.jinja2",
        template="form-template",
        title="Page coming soon"
    )

@app.route("/success", methods=["GET", "POST"])
def success():
    """Generic success page upon form submission."""
    return render_template(
        "success.jinja2",
        template="success-template"
    )
