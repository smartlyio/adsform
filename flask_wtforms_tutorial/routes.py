"""Routing."""
from flask import current_app as app
from flask import request, redirect, render_template, url_for, jsonify
import json
from .forms import AdForm, SignupForm


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
    form = AdForm()
    if form.validate_on_submit():
        # upload file to google drive
        # push data into google sheet
        return redirect(url_for("success"))
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
