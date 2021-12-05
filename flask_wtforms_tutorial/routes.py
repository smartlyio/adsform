"""Routing."""
from flask import current_app as app
from flask import request, redirect, render_template, url_for, jsonify
from .forms import AdForm
from .googleint import *
from .data_fetcher import *
from datetime import datetime, date
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
        if att:
            for madia_upload in att: #picture_upload
                currentfile = att[0]
                filename = currentfile.filename
                media_contents = madia_upload.stream.read()
                
                # upload file to google drive
                media_url = write_into_drive(media_contents, currentfile)
                
                file_type = "image" if (currentfile.mimetype == "image/jpeg" or currentfile.mimetype == "image/png" or currentfile.mimetype == "image/svg") else "video"
                video_length = "na" if(file_type == "image" ) else get_video_duration(filename)
                mediasize = get_image_size(filename) if(file_type == "image" ) else get_video_size(filename)
                start_date = "" if (form['startdate'].data == date(1111,11,11)) else form['startdate'].data.strftime('%m/%d/%Y')
                end_date = "" if (form['enddate'].data == date(1111,11,11)) else form['enddate'].data.strftime('%m/%d/%Y')
                coordinates = get_coordinates(form['city'].data)
                
                # [ID,language, adFormat, copy, title, CTA, startDate, endDate, creativeType, conceptName, adName, 
                # mediaSize, videoLength, mediaURL, country, city, UA or R&F, coordinates, Live, facebook page, IG account]
                ad_data = [
                    datetime.now().strftime("%c"),
                    form['language'].data,
                    file_type,
                    form['adcopy'].data,
                    form['adtitle'].data,
                    form['calltoaction'].data,
                    start_date,
                    end_date,
                    form['creativetype'].data,
                    form['creativeconcept'].data,
                    form['adname'].data,
                    mediasize, # mediasize
                    video_length, # video length (na for images)
                    media_url,
                    form['country'].data,
                    form['city'].data,
                    form['objective'].data, # UA or R&F or both
                    coordinates # coordinates
                    # fb page id, filled in the sheet with a vlookup
                    # instagram id, filled in the sheet with a vlookup
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
