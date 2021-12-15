"""Routing."""
from flask import current_app as app
from flask import request, redirect, render_template, url_for, jsonify
from .forms import AdForm
from .googleint import *
from datetime import datetime, date
from werkzeug.utils import secure_filename
import logging
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
			with open('countries_cities.json') as fp:
				data = json.load(fp)
			return jsonify(result=data[countryId])
		else:
			return jsonify(result=[''])
	except Exception as e:
		return str(e)

@app.route("/createad", methods=["GET", "POST"])
def createad():
	try:
		"""Create ads"""
		form = AdForm(request.form)
		logging.warning('starting createad')
		if form.validate_on_submit():
			att = request.files.getlist(form.attachment.name)
			if att:
				for madia_upload in att:
					currentfile = att[0]
					filename = secure_filename(currentfile.filename)
					media_contents = madia_upload.stream.read()
					
					# upload file to google drive
					media_url = write_into_drive(media_contents, currentfile, filename)
					logging.warning("written into google drive!")
					logging.warning(media_url)
					file_type = "image" if (currentfile.mimetype == "image/jpeg" or currentfile.mimetype == "image/png" or currentfile.mimetype == "image/svg") else "video"
					video_length = "na" if(file_type == "image" ) else get_video_duration(filename)
					mediasize = get_image_size(filename) if(file_type == "image" ) else get_video_size(filename)
					start_date = "" if (form['startdate'].data == date(1111,11,11)) else form['startdate'].data.strftime('%m/%d/%Y') #encountered what seems to be a bug in validation of empty values in wtforms
					end_date = "" if (form['enddate'].data == date(1111,11,11)) else form['enddate'].data.strftime('%m/%d/%Y')
					logging.warning('so far so good 1')
					logging.warning("so far so good 1")
					# remove from local temp file
					if os.path.exists('temp/' + filename):
						os.remove('temp/' + filename)
					remaining = len(form['city'].data)
					for city in form['city'].data:
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
							mediasize,
							video_length,
							media_url,
							form['country'].data,
							city,
							form['objective'].data, # UA or R&F or both
						]
						logging.warning("attempting a write into sheets")
						write_status = write_into_sheet(ad_data)
						remaining -= 1
						logging.warning("written into sheet, hopefully")
						if write_status != 'ok':
							return render_template(
							"adcreation.jinja2",
							form=form,
							template="form-template",
							title="Create Ad Form"
						)
						elif write_status == 'ok' and remaining == 0:
							return redirect(url_for("success"))
			else:
				logging.warning('something bad happened.')
				return render_template(
				"adcreation.jinja2",
				form=form,
				template="form-template",
				title="Create Ad Form"
			)

	except Exception as e:	
		logging.warning('something bad happened. Again.')
		logging.warning(str(e))
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