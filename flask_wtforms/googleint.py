import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.utils import secure_filename
from PIL import Image
from pathlib import Path
from io import BytesIO
import os
import json
import cv2
import logging
from google.oauth2.service_account import Credentials
from google.cloud import secretmanager
import datetime

vertical_dimensions = [1920, 1620, 1350]


def write_into_sheet(ad_data):
	try:
		credentials = retrieve_credentials()
		logging.warning("ran get credentials from service account")
		gs = gspread.authorize(credentials)
		logging.warning("authorized gspread!")
		worksheet = gs.open_by_key("1gf6SCpqDZDxFSqeXyXjGwS0vPHgNQjTWYEm1WYeJPi4").worksheet("Form")
		# test worksheet = gs.open_by_key("1fn0g53MbdpVRpkzaHEpWsjkN5_oHLepVmbh45veKhqI").worksheet("Form")
		next_row = next_available_row(worksheet)
		logging.warning('next_available_row :')
		logging.warning(next_row)
		row_to_begin = "A{}".format(next_row)
		worksheet.update(row_to_begin, ad_data)
		return "ok"
	except Exception as e:
		logging.warning('An error occurred while writing to the sheet', e)
		return "error"

def get_secrets():
	logging.warning('in get_secrets')
	client = secretmanager.SecretManagerServiceClient()
	logging.warning('secretmanager.SecretManagerServiceClient ran OK')
	jsonPl = client.access_secret_version(
                request={"name": f"projects/927617313118/secrets/feed-form/versions/latest"}
            ).payload.data.decode("UTF-8")
	logging.warning('got jsonPl')
	myjson = json.loads(jsonPl)
	return json.loads(jsonPl)


def retrieve_credentials():
    secrets = get_secrets()
    logging.warning('get secrets ran ok')
    scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
	]
    service_account_credentials = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scopes=scope)
    logging.warning('get credentials from serv acc info ran ok')
    return service_account_credentials

def next_available_row(worksheet):
	str_list = list(filter(None, worksheet.col_values(1)))
	return str(len(str_list)+1)


def write_into_drive(filebytes, file, filename):
	try:
		logging.warning('trying to write into drive')
		gauth = GoogleAuth()
		gauth.auth_method = 'service'
		logging.warning('got gauth')
		credentials = retrieve_credentials()
		logging.warning('retrieved credentials')
		gauth.credentials = credentials
		drive = GoogleDrive(gauth)
		logging.warning("google drive initialised with credentials")
		drive_file = drive.CreateFile({'title': filename,
							  'mimeType': file.mimetype,
		})

		logging.warning("starting to add temporary local file")
		Path("temp").mkdir(exist_ok=True)
		if not os.path.exists('temp/' + filename):
			logging.warning("attempting adding temp file")
			if (file.mimetype == "image/jpeg" or file.mimetype == "image/png" or file.mimetype == "image/svg"):
				image = Image.open(BytesIO(filebytes))
				image.save('temp/' + filename)
				logging.warning("image SAVED")
				image.close()
			else :
				open('temp/'+filename, 'wb').write(filebytes)

		logging.warning("completed adding temporary local file")
		drive_file.SetContentFile('temp/'+filename)
		drive_file.Upload()
		# SET PERMISSION todo ceren review this idea
		drive_file.InsertPermission({
									'type': 'anyone',
									'value': 'anyone',
									'role': 'reader'})

		# SHARABLE LINK
		link=drive_file['alternateLink']

		# To use the image in Gsheet we need to modify the link as follows
		link=drive_file['alternateLink']
		link=link.split('?')[0]
		link=link.split('/')[-2]
		link='https://docs.google.com/uc?export=download&id='+link
		
		logging.warning("HERE IS THE DRIVE LINK ->")
		logging.warning(link)
		return link

	except Exception as e:
		logging.warning('ERROR when uploading to drive:', str(e))
		return ''

def get_image_size(filename):
	try:
		im = Image.open("temp/"+filename)
		w, h = im.size
		return (w,h)
	except Exception as e:
		logging.warning("couldn't get media size for image {} with error {}".format(filename, str(e)))
		return ""

def get_image_size_name(width, height):
	try: 
		if (width == height):
			return "square"
		elif (width == 1080 and height in vertical_dimensions):
			return 'vertical'
	except Exception as e:
		logging.warning("Couldn't decide a ratio name for dimensions {}x{} with error {}, falling back to square".format(width, height, str(e)))
		return "square"

def get_video_size(filename):
	try:
		vid = cv2.VideoCapture('temp/' + filename)
		height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
		width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
		return ('{}x{}').format(width,height)
	except Exception as e:
		logging.warning("couldn't get media size for video {} with error {}".format(filename, str(e)))
		return ""

# https://stackoverflow.com/questions/49048111/how-to-get-the-duration-of-video-using-cv2
# seek to the end, then get the timestamp to find the length of the stream
def get_video_duration(filename):
	try:
		vid = cv2.VideoCapture('temp/' + filename)
		# count the number of frames
		frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
		fps = int(vid.get(cv2.CAP_PROP_FPS))

		# calculate dusration of the video
		seconds = int(frames / fps) + 1
		# video_time = str(datetime.timedelta(seconds=seconds))
		return str(seconds) + "s"
	except Exception as e:
		logging.warning("couldn't get video length for file {} with error {}".format(filename, str(e)))
		return ""