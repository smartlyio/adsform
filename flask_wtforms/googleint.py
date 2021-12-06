import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import os
import cv2
import datetime

def write_into_sheet(ad_data):
	try:
		gc = gspread.service_account(
			filename='flask_wtforms/service_account.json')
		sh = gc.open("Facebook Ads Express - Wolt")
		worksheet = sh.sheet1
		next_row = next_available_row(worksheet)
		row_to_begin = "A{}".format(next_row)
		worksheet.update(row_to_begin, [ad_data])
		return "ok"
	except Exception as e:
		print('An error occurred while writing to the sheet', e)
		return "error"


def next_available_row(worksheet):
	str_list = list(filter(None, worksheet.col_values(1)))
	return str(len(str_list)+1)


def write_into_drive(filebytes, file, filename):
	try:
		gauth = GoogleAuth()
		scope = ["https://www.googleapis.com/auth/drive"]
		gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
			'flask_wtforms/service_account.json', scope)
		drive = GoogleDrive(gauth)
		drive_file = drive.CreateFile({'title': filename,
							  'mimeType': file.mimetype,
		})

		if not os.path.exists('temp/' + filename):
			if (file.mimetype == "image/jpeg" or file.mimetype == "image/png" or file.mimetype == "image/svg"):
				image = Image.open(BytesIO(filebytes))
				image.save('temp/' + filename)
				image.close()
			else :
				open('temp/'+filename, 'wb').write(filebytes)

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

		return link

	except Exception as e:
		print('ERROR when uploading to drive:', str(e))
		return ''

def get_image_size(filename):
	try:
		im = Image.open("temp/"+filename)

		print(im.size)
		print(type(im.size))

		w, h = im.size
		print('width: ', w)
		print('height:', h)
		return ("{}x{}").format(w,h)
	except Exception as e:
		print("couldn't get media size for image {} with error {}").format(filename, str(e))
		return ""

def get_video_size(filename):
	try:
		vid = cv2.VideoCapture('temp/' + filename)
		height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
		width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
		return ('{}x{}').format(width,height)
	except Exception as e:
		print("couldn't get media size for video {} with error {}").format(filename, str(e))
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
		seconds = int(frames / fps)
		video_time = str(datetime.timedelta(seconds=seconds))
		return video_time
	except Exception as e:
		print ("couldn't get video length for file {} with error {}").format(filename, str(e))
		return ""