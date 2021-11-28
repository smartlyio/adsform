# Ads Form
Used WTF forms, Jinja for templating

Check https://github.com/hackersandslackers/flask-wtform-tutorial for a base template if needed

# Getting Started

Get set up locally:

### Installation

Get up and running with `make deploy`:

```shell
$ git clone https://github.com/cerentuker/adsform
$ cd flask-wtform-tutorial
$ make deploy
``` 

OR 

```shell
$ python3 -m venv .venv
$ . .venv/bin/activate 
$ flask run
``` 

### Environment Variables

Replace the values in **.env.example** with your values and rename this file to **.env**:

* `FLASK_APP`: Entry point of your application (should be `wsgi.py`).
* `FLASK_ENV`: The environment to run your app in (either `development` or `production`).
* `SECRET_KEY`: Randomly generated string of characters used to encrypt your app's data.

*Remember never to commit secrets saved in .env files to Github.*

