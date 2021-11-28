"""Routing."""
from flask import current_app as app
from flask import redirect, render_template, url_for

from .forms import ContactForm, SignupForm


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        template="home-template",
        title="Ad Creator Form App"
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "contact.jinja2",
        form=form,
        template="form-template",
        title="Contact Form"
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
