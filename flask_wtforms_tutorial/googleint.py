import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from io import BytesIO
import os
import subprocess

def write_into_sheet(ad_data):
    try:
        gc = gspread.service_account(filename='flask_wtforms_tutorial/service_account.json')
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


def write_into_drive(filebytes, file):
    try:    
        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('flask_wtforms_tutorial/service_account.json', scope)
        drive = GoogleDrive(gauth)
        drive_file = drive.CreateFile({'title':file.filename,
                              'mimeType': file.mimetype,
        })

        if not os.path.exists('temp/' + file.filename):
                image = Image.open(BytesIO(filebytes))
                image.save('temp/' + file.filename)
                image.close()

        drive_file.SetContentFile('temp/' + file.filename)
        drive_file.Upload()
        #SET PERMISSION todo ceren review this idea
        drive_file.InsertPermission({
                                    'type': 'anyone',
                                    'value': 'anyone',
                                    'role': 'reader'})

        #SHARABLE LINK
        link=drive_file['alternateLink']

        #To use the image in Gsheet we need to modify the link as follows
        link=drive_file['alternateLink']
        link=link.split('?')[0]
        link=link.split('/')[-2]
        link='https://docs.google.com/uc?export=download&id='+link
        return link
    except Exception as e:
        print('ERROR when uploading to drive:', str(e))
        return ''

def get_media_size(filename):
    try:
        im = Image.open("temp/"+filename)

        print(im.size)
        print(type(im.size))

        w, h = im.size
        print('width: ', w)
        print('height:', h)
        return ("{}x{}").format(w,h)
    except:
        print("couldnt get media size for image {}").format(filename)
        return ""


def get_video_duration(filename):
    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", 'temp/'+filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
    except:
        print("couldnt get video length for file {}").format(filename)
        return ""