from flask import current_app as app
import requests
from flask import request

@app.route('/getcountrycities', methods=["GET"])
def get_cities():
    country = request.args.get('country')
    payload = {'country': country}
    response = requests.get('http://wolt-geofencing-dot-feeds-233607.appspot.com/country/cities', params=payload) if (country != None) else requests.get('http://wolt-geofencing-dot-feeds-233607.appspot.com/country/cities')
    if (response.status_code != '200'):
     return response.text
    else:
     return []

@app.route('/fillcountries', methods=["GET"])
def get_all_countries():
    response = requests.get('http://wolt-geofencing-dot-feeds-233607.ew.r.appspot.com/countries')
    if (response.status_code != '200'):
     return response.json()
    else:
     return []